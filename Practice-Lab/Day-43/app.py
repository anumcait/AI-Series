import os
import json
import sqlite3
from datetime import datetime, timezone, timedelta

import boto3
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from dotenv import load_dotenv
from botocore.exceptions import ClientError, BotoCoreError

load_dotenv()

DB = "security_audit.db"
PROFILE = os.getenv("AWS_PROFILE", "default")
MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")
OLLAMA_URL = "http://localhost:11434/api/generate"

SENSITIVE_PORTS = {
    22, 3389, 3306, 5432, 1433, 1521,
    27017, 6379, 9200
}


def db_connection():
    return sqlite3.connect(DB)


def initialize_db():
    with db_connection() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_time TEXT,
                region TEXT,
                service TEXT,
                resource TEXT,
                severity TEXT,
                issue TEXT,
                recommendation TEXT
            )
        """)


def add_finding(findings, service, resource, severity,
                issue, recommendation):
    findings.append({
        "Service": service,
        "Resource": str(resource),
        "Severity": severity,
        "Issue": issue,
        "Recommendation": recommendation
    })


def audit_s3(session, findings, errors):
    s3 = session.client("s3")

    try:
        buckets = s3.list_buckets().get("Buckets", [])
    except (ClientError, BotoCoreError) as exc:
        errors.append(f"S3 bucket listing: {exc}")
        return

    for bucket in buckets:
        name = bucket["Name"]

        try:
            acl = s3.get_bucket_acl(Bucket=name)
            public_acl = any(
                grant.get("Grantee", {}).get("URI", "").endswith(
                    ("AllUsers", "AuthenticatedUsers")
                )
                for grant in acl.get("Grants", [])
            )

            policy_public = False
            try:
                policy_public = s3.get_bucket_policy_status(
                    Bucket=name
                ).get("PolicyStatus", {}).get("IsPublic", False)
            except ClientError as exc:
                if exc.response["Error"]["Code"] not in (
                    "NoSuchBucketPolicy", "NoSuchBucketPolicyStatus"
                ):
                    raise

            if public_acl or policy_public:
                add_finding(
                    findings, "S3", name, "Critical",
                    "Bucket ACL or bucket policy indicates public access.",
                    "Review bucket ACL and policy. Remove unintended public access."
                )

            try:
                block = s3.get_public_access_block(
                    Bucket=name
                )["PublicAccessBlockConfiguration"]

                if not all(block.get(key, False) for key in (
                    "BlockPublicAcls",
                    "IgnorePublicAcls",
                    "BlockPublicPolicy",
                    "RestrictPublicBuckets"
                )):
                    add_finding(
                        findings, "S3", name, "High",
                        "One or more S3 Public Access Block settings are disabled.",
                        "Enable all four account-appropriate bucket public access block settings."
                    )
            except ClientError as exc:
                if exc.response["Error"]["Code"] == (
                    "NoSuchPublicAccessBlockConfiguration"
                ):
                    add_finding(
                        findings, "S3", name, "High",
                        "Bucket has no explicit Public Access Block configuration.",
                        "Review exposure and configure S3 Block Public Access."
                    )
                else:
                    raise

        except (ClientError, BotoCoreError) as exc:
            errors.append(f"S3 bucket {name}: {exc}")


def audit_ec2(session, region, findings, errors):
    ec2 = session.client("ec2", region_name=region)

    try:
        groups = ec2.describe_security_groups()["SecurityGroups"]

        for group in groups:
            for permission in group.get("IpPermissions", []):
                protocol = permission.get("IpProtocol")
                from_port = permission.get("FromPort", -1)
                to_port = permission.get("ToPort", -1)

                if protocol == "-1":
                    sensitive = True
                    port_text = "all ports"
                else:
                    sensitive = any(
                        from_port <= port <= to_port
                        for port in SENSITIVE_PORTS
                    )
                    port_text = f"{from_port}-{to_port}"

                if not sensitive:
                    continue

                public_sources = []

                for item in permission.get("IpRanges", []):
                    if item.get("CidrIp") == "0.0.0.0/0":
                        public_sources.append("0.0.0.0/0")

                for item in permission.get("Ipv6Ranges", []):
                    if item.get("CidrIpv6") == "::/0":
                        public_sources.append("::/0")

                if public_sources:
                    add_finding(
                        findings, "EC2 Security Group",
                        group["GroupId"], "High",
                        f"Sensitive inbound access ({port_text}) is open to "
                        f"{', '.join(public_sources)}.",
                        "Restrict inbound rules to approved IP addresses and required ports."
                    )

    except (ClientError, BotoCoreError) as exc:
        errors.append(f"EC2 security groups: {exc}")

    try:
        volumes = ec2.describe_volumes()["Volumes"]

        for volume in volumes:
            if not volume.get("Encrypted", False):
                add_finding(
                    findings, "EBS", volume["VolumeId"], "Medium",
                    "EBS volume is not encrypted.",
                    "Plan a migration or snapshot-and-recreate process using encryption."
                )

    except (ClientError, BotoCoreError) as exc:
        errors.append(f"EBS volumes: {exc}")


def audit_rds(session, region, findings, errors):
    rds = session.client("rds", region_name=region)

    try:
        paginator = rds.get_paginator("describe_db_instances")

        for page in paginator.paginate():
            for db in page["DBInstances"]:
                if db.get("PubliclyAccessible", False):
                    add_finding(
                        findings, "RDS", db["DBInstanceIdentifier"], "High",
                        "RDS instance is configured as publicly accessible.",
                        "Review the network design and disable public accessibility if unnecessary."
                    )

    except (ClientError, BotoCoreError) as exc:
        errors.append(f"RDS: {exc}")


def audit_iam(session, findings, errors):
    iam = session.client("iam")
    now = datetime.now(timezone.utc)

    try:
        paginator = iam.get_paginator("list_users")

        for page in paginator.paginate():
            for user in page["Users"]:
                username = user["UserName"]

                try:
                    keys = iam.list_access_keys(
                        UserName=username
                    )["AccessKeyMetadata"]

                    for key in keys:
                        created = key["CreateDate"]
                        age = (now - created).days

                        if key["Status"] == "Active" and age > 90:
                            add_finding(
                                findings, "IAM", username, "Medium",
                                f"Active access key is {age} days old.",
                                "Review key usage and rotate old keys according to policy."
                            )

                    mfa = iam.list_mfa_devices(
                        UserName=username
                    )["MFADevices"]

                    if not mfa:
                        add_finding(
                            findings, "IAM", username, "Medium",
                            "IAM user has no MFA device registered.",
                            "Enable MFA where appropriate and review whether the user needs console access."
                        )

                except (ClientError, BotoCoreError) as exc:
                    errors.append(f"IAM user {username}: {exc}")

    except (ClientError, BotoCoreError) as exc:
        errors.append(f"IAM users: {exc}")


def audit_cloudtrail(session, region, findings, errors):
    ct = session.client("cloudtrail", region_name=region)

    try:
        trails = ct.describe_trails(
            includeShadowTrails=True
        ).get("trailList", [])

        if not trails:
            add_finding(
                findings, "CloudTrail", region, "High",
                "No CloudTrail trail was discovered.",
                "Configure an appropriate multi-region CloudTrail trail."
            )
            return

        for trail in trails:
            name = trail["Name"]

            try:
                status = ct.get_trail_status(Name=name)

                if not status.get("IsLogging", False):
                    add_finding(
                        findings, "CloudTrail", name, "High",
                        "CloudTrail trail is not actively logging.",
                        "Review the trail and enable logging if required."
                    )

            except (ClientError, BotoCoreError) as exc:
                errors.append(f"CloudTrail status {name}: {exc}")

    except (ClientError, BotoCoreError) as exc:
        errors.append(f"CloudTrail: {exc}")


def run_audit(region):
    session = boto3.Session(profile_name=PROFILE)
    findings, errors = [], []

    identity = session.client("sts").get_caller_identity()

    audit_s3(session, findings, errors)
    audit_ec2(session, region, findings, errors)
    audit_rds(session, region, findings, errors)
    audit_iam(session, findings, errors)
    audit_cloudtrail(session, region, findings, errors)

    audit_time = datetime.now(timezone.utc).isoformat()

    with db_connection() as con:
        for item in findings:
            con.execute("""
                INSERT INTO findings
                (audit_time, region, service, resource,
                 severity, issue, recommendation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                audit_time, region, item["Service"],
                item["Resource"], item["Severity"],
                item["Issue"], item["Recommendation"]
            ))

    return identity, findings, errors, audit_time


def ai_analysis(findings):
    if not findings:
        return "No findings were returned by the completed checks."

    prompt = f"""
You are an AWS cloud security assistant.
Explain these audit findings in clear language.
Group risks by severity. Explain the possible impact
and provide safe, practical remediation steps.
Do not claim that a resource is compromised.
Do not execute or suggest automatic changes.

Findings:
{json.dumps(findings, indent=2)}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )
    response.raise_for_status()
    return response.json().get("response", "")


st.set_page_config(
    page_title="AWS Security Auditor",
    page_icon="🔐",
    layout="wide"
)

initialize_db()

st.title("🔐 Local AI-Powered AWS Security Auditor")
st.caption("Read-only AWS checks • Local Qwen3 analysis • SQLite audit history")

region = st.text_input(
    "AWS region to scan",
    value=os.getenv("AWS_DEFAULT_REGION", "ap-south-1")
)

if st.button("🔍 Run AWS Security Audit", type="primary"):
    try:
        with st.spinner("Inspecting AWS security configurations..."):
            identity, findings, errors, audit_time = run_audit(region)

        st.session_state["findings"] = findings
        st.session_state["errors"] = errors
        st.session_state["identity"] = identity
        st.session_state["audit_time"] = audit_time

        st.success("Audit checks completed. Review findings and scan errors.")

    except Exception as exc:
        st.error(f"Audit could not start: {exc}")

findings = st.session_state.get("findings", [])
errors = st.session_state.get("errors", [])

if "identity" in st.session_state:
    st.write(
        f"**AWS Account:** {st.session_state['identity'].get('Account')}  "
        f" | **Region:** {region}"
    )
    st.caption(f"Last audit: {st.session_state.get('audit_time')}")

if findings:
    df = pd.DataFrame(findings)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total findings", len(df))
    c2.metric("Critical", int((df["Severity"] == "Critical").sum()))
    c3.metric("High", int((df["Severity"] == "High").sum()))
    c4.metric("Medium", int((df["Severity"] == "Medium").sum()))

    st.subheader("Security Findings")
    st.dataframe(df, use_container_width=True)

    chart = px.histogram(
        df, x="Severity", color="Severity",
        title="Findings by Severity"
    )
    st.plotly_chart(chart, use_container_width=True)

    st.download_button(
        "Download current audit CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="aws_security_findings.csv",
        mime="text/csv"
    )

    if st.button("🤖 Analyze Findings with Local Qwen3"):
        try:
            with st.spinner("Qwen3 is analyzing the findings..."):
                analysis = ai_analysis(findings)
            st.session_state["ai_analysis"] = analysis
        except Exception as exc:
            st.error(f"AI analysis failed: {exc}")

    if "ai_analysis" in st.session_state:
        st.subheader("AI Security Analysis")
        st.markdown(st.session_state["ai_analysis"])

elif "findings" in st.session_state:
    st.success("No findings were returned by the completed checks.")

if errors:
    st.subheader("Checks requiring attention")
    st.warning(
        "Some checks could not be completed. Do not interpret these "
        "as passing security checks."
    )
    for error in errors:
        st.write(f"- {error}")

st.divider()
st.subheader("Audit History")

with db_connection() as con:
    history = pd.read_sql_query(
        "SELECT * FROM findings ORDER BY audit_time DESC LIMIT 500",
        con
    )

if not history.empty:
    st.dataframe(history, use_container_width=True)
else:
    st.info("No historical findings have been stored yet.")