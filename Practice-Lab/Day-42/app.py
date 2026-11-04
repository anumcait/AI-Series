import os
import json
import sqlite3
from datetime import date, datetime, timedelta, timezone

import boto3
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from botocore.exceptions import BotoCoreError, ClientError


# ---------------- CONFIGURATION ----------------

DB_FILE = "finops.db"
MODEL = "qwen3:4b"
OLLAMA_URL = "http://localhost:11434/api/generate"

REGION = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")
PROFILE = os.getenv("AWS_PROFILE", "default")

CPU_IDLE_LIMIT = 5.0
COST_SPIKE_MULTIPLIER = 1.5


# ---------------- DATABASE ----------------

def db_connection():
    return sqlite3.connect(DB_FILE)


def initialize_db():
    with db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collected_at TEXT,
                total_cost REAL,
                idle_instances INTEGER,
                unattached_volumes INTEGER,
                estimated_monthly_cost REAL
            )
        """)


def save_snapshot(total_cost, idle_count, volume_count, estimate):
    with db_connection() as conn:
        conn.execute("""
            INSERT INTO snapshots
            (collected_at, total_cost, idle_instances,
             unattached_volumes, estimated_monthly_cost)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(),
            total_cost,
            idle_count,
            volume_count,
            estimate
        ))


def load_history():
    with db_connection() as conn:
        return pd.read_sql_query(
            "SELECT * FROM snapshots ORDER BY id",
            conn
        )


# ---------------- AWS CONNECTION ----------------

@st.cache_resource
def aws_session():
    return boto3.Session(
        profile_name=PROFILE,
        region_name=REGION
    )


def collect_aws_data():
    session = aws_session()

    ce = session.client("ce", region_name="us-east-1")
    ec2 = session.client("ec2")
    cloudwatch = session.client("cloudwatch")

    end_date = date.today()
    start_date = end_date - timedelta(days=60)

    cost_response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": start_date.isoformat(),
            "End": end_date.isoformat()
        },
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
    )

    cost_rows = []

    for day in cost_response["ResultsByTime"]:
        for group in day["Groups"]:
            cost_rows.append({
                "Date": day["TimePeriod"]["Start"],
                "Service": group["Keys"][0],
                "Cost": float(
                    group["Metrics"]["UnblendedCost"]["Amount"]
                )
            })

    costs = pd.DataFrame(
        cost_rows,
        columns=["Date", "Service", "Cost"]
    )

    # Retrieve EC2 inventory
    instances = []

    paginator = ec2.get_paginator("describe_instances")

    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                name = next(
                    (
                        tag["Value"]
                        for tag in instance.get("Tags", [])
                        if tag["Key"] == "Name"
                    ),
                    "Unnamed"
                )

                instance_id = instance["InstanceId"]
                state = instance["State"]["Name"]
                instance_type = instance["InstanceType"]

                cpu_values = []

                # CPU analysis only for running instances
                if state == "running":
                    result = cloudwatch.get_metric_statistics(
                        Namespace="AWS/EC2",
                        MetricName="CPUUtilization",
                        Dimensions=[
                            {
                                "Name": "InstanceId",
                                "Value": instance_id
                            }
                        ],
                        StartTime=datetime.now(timezone.utc)
                        - timedelta(days=7),
                        EndTime=datetime.now(timezone.utc),
                        Period=3600,
                        Statistics=["Average"]
                    )

                    cpu_values = [
                        point["Average"]
                        for point in result["Datapoints"]
                    ]

                average_cpu = (
                    sum(cpu_values) / len(cpu_values)
                    if cpu_values else None
                )

                instances.append({
                    "Name": name,
                    "InstanceId": instance_id,
                    "Type": instance_type,
                    "State": state,
                    "AverageCPU": average_cpu
                })

    instance_df = pd.DataFrame(
        instances,
        columns=[
            "Name", "InstanceId", "Type",
            "State", "AverageCPU"
        ]
    )

    # Retrieve EBS inventory
    volumes_response = ec2.describe_volumes()
    volume_rows = []

    for volume in volumes_response["Volumes"]:
        volume_rows.append({
            "VolumeId": volume["VolumeId"],
            "SizeGB": volume["Size"],
            "State": volume["State"],
            "VolumeType": volume["VolumeType"],
            "Unattached": len(volume.get("Attachments", [])) == 0
        })

    volumes = pd.DataFrame(
        volume_rows,
        columns=[
            "VolumeId", "SizeGB", "State",
            "VolumeType", "Unattached"
        ]
    )

    return costs, instance_df, volumes


# ---------------- FINOPS ANALYSIS ----------------

def analyze_costs(costs):
    if costs.empty:
        return 0.0, 0.0, pd.DataFrame()

    daily = (
        costs.groupby("Date", as_index=False)["Cost"]
        .sum()
        .sort_values("Date")
    )

    total_cost = float(daily["Cost"].sum())

    # Estimate based on observed daily spending.
    # This is not an AWS forecast.
    elapsed_days = max(
        (date.today() - date.fromisoformat(
            daily["Date"].min()
        )).days,
        1
    )

    monthly_estimate = (
        total_cost / elapsed_days
    ) * 60

    if len(daily) >= 8:
        daily["Previous7DayAverage"] = (
            daily["Cost"].shift(1).rolling(7).mean()
        )

        daily["CostAnomaly"] = (
            daily["Cost"]
            > daily["Previous7DayAverage"]
            * COST_SPIKE_MULTIPLIER
        )
    else:
        daily["Previous7DayAverage"] = None
        daily["CostAnomaly"] = False

    return total_cost, monthly_estimate, daily


def find_recommendations(instances, volumes, daily):
    findings = []

    if not instances.empty:
        idle = instances[
            (instances["State"] == "running")
            & (instances["AverageCPU"].notna())
            & (instances["AverageCPU"] < CPU_IDLE_LIMIT)
        ]

        for _, item in idle.iterrows():
            findings.append({
                "Type": "Potentially idle EC2",
                "Resource": item["InstanceId"],
                "Finding": (
                    f"Average CPU is {item['AverageCPU']:.2f}% "
                    "over the available seven-day metric window."
                ),
                "Recommendation": (
                    "Review workload and business requirements. "
                    "Consider rightsizing or scheduling only after validation."
                )
            })

    if not volumes.empty:
        unattached = volumes[volumes["Unattached"] == True]

        for _, item in unattached.iterrows():
            findings.append({
                "Type": "Unattached EBS volume",
                "Resource": item["VolumeId"],
                "Finding": (
                    f"{item['SizeGB']} GB volume is not attached "
                    "to an EC2 instance."
                ),
                "Recommendation": (
                    "Check snapshots, backups, and ownership. "
                    "Delete only after explicit approval."
                )
            })

    if not daily.empty:
        anomalies = daily[daily["CostAnomaly"] == True]

        for _, item in anomalies.iterrows():
            findings.append({
                "Type": "Daily cost spike",
                "Resource": item["Date"],
                "Finding": (
                    f"Daily cost {item['Cost']:.2f} is above "
                    "1.5 times the preceding seven-day average."
                ),
                "Recommendation": (
                    "Review service-wise spending and recent deployments."
                )
            })

    return pd.DataFrame(
        findings,
        columns=[
            "Type", "Resource", "Finding", "Recommendation"
        ]
    )


# ---------------- LOCAL AI ----------------

def ask_ai(context):
    prompt = f"""
You are a cloud FinOps assistant.

Analyze the AWS findings below.

Rules:
- Use only the supplied evidence.
- Do not invent prices or savings.
- Explain why each finding matters.
- Suggest practical investigation steps.
- Never recommend deleting or stopping resources without validation.
- Clearly distinguish confirmed facts from possible causes.
- Do not claim a resource is wasteful based only on low CPU.

AWS FINDINGS:
{json.dumps(context, indent=2)}

Return:
1. Overall cost summary
2. Important findings
3. Possible causes
4. Recommended actions
5. Risks and validation steps
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
    return response.json()["response"]


# ---------------- STREAMLIT APP ----------------

st.set_page_config(
    page_title="Local AI FinOps Assistant",
    page_icon="☁️",
    layout="wide"
)

initialize_db()

st.title("☁️ Local AI Cloud Cost Optimization Assistant")
st.caption(
    "AWS FinOps | Cost Analysis | Resource Optimization | Local AI"
)

st_autorefresh(interval=300000, key="dashboard_refresh")

if st.button("🔄 Refresh AWS Data"):
    st.cache_resource.clear()
    st.rerun()

try:
    with st.spinner("Collecting latest available AWS data..."):
        costs, instances, volumes = collect_aws_data()

    total_cost, monthly_estimate, daily = analyze_costs(costs)

    findings = find_recommendations(
        instances, volumes, daily
    )

    idle_count = (
        len(instances[
            (instances["State"] == "running")
            & (instances["AverageCPU"].notna())
            & (instances["AverageCPU"] < CPU_IDLE_LIMIT)
        ])
        if not instances.empty else 0
    )

    unattached_count = (
        int(volumes["Unattached"].sum())
        if not volumes.empty else 0
    )

    save_snapshot(
        total_cost,
        idle_count,
        unattached_count,
        monthly_estimate
    )

    st.success(
        f"Data collected successfully | "
        f"Region: {REGION} | "
        f"Updated: {datetime.now().strftime('%H:%M:%S')}"
    )

    # Summary cards
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Last 60-day cost", f"${total_cost:,.2f}")
    c2.metric("Estimated 60-day spend", f"${monthly_estimate:,.2f}")
    c3.metric("Potentially idle EC2", idle_count)
    c4.metric("Unattached EBS", unattached_count)

    st.divider()

    # Cost charts
    st.subheader("📊 AWS Cost Analysis")

    if not costs.empty:
        service_cost = (
            costs.groupby("Service", as_index=False)["Cost"]
            .sum()
            .sort_values("Cost", ascending=False)
        )

        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                px.line(
                    daily,
                    x="Date",
                    y="Cost",
                    title="Daily AWS Spending"
                ),
                use_container_width=True
            )

        with right:
            st.plotly_chart(
                px.bar(
                    service_cost,
                    x="Service",
                    y="Cost",
                    title="Service-wise AWS Cost"
                ),
                use_container_width=True
            )

        st.dataframe(daily, use_container_width=True)
    else:
        st.info("No cost data was returned for this period.")

    st.divider()

    # Infrastructure
    st.subheader("🖥️ EC2 Infrastructure")

    st.dataframe(instances, use_container_width=True)

    st.subheader("💾 EBS Volumes")

    st.dataframe(volumes, use_container_width=True)

    st.divider()

    # Findings
    st.subheader("🔍 Cost Optimization Findings")

    if findings.empty:
        st.info("No findings detected by the current rules.")
    else:
        st.dataframe(findings, use_container_width=True)

    st.download_button(
        "Download findings CSV",
        findings.to_csv(index=False),
        "finops_findings.csv",
        "text/csv"
    )

    st.download_button(
        "Download cost data CSV",
        costs.to_csv(index=False),
        "aws_costs.csv",
        "text/csv"
    )

    # AI analysis
    st.divider()
    st.subheader("🤖 Local AI FinOps Analysis")

    if st.button("Analyze findings using Qwen3"):
        context = {
            "region": REGION,
            "total_cost": total_cost,
            "estimated_monthly_cost": monthly_estimate,
            "cost_anomalies": (
                daily[daily["CostAnomaly"] == True].to_dict("records")
                if not daily.empty else []
            ),
            "findings": findings.to_dict("records")
        }

        with st.spinner("Qwen3 is analyzing the findings..."):
            try:
                result = ask_ai(context)
                st.session_state["ai_result"] = result
            except requests.RequestException as error:
                st.error(f"Ollama request failed: {error}")

    if "ai_result" in st.session_state:
        st.markdown(st.session_state["ai_result"])

    # History
    st.divider()
    st.subheader("📚 Monitoring History")

    history = load_history()

    if not history.empty:
        st.dataframe(history, use_container_width=True)

        st.plotly_chart(
            px.line(
                history,
                x="collected_at",
                y="total_cost",
                title="Collected Cost Snapshots"
            ),
            use_container_width=True
        )

except (ClientError, BotoCoreError) as error:
    st.error(f"AWS connection or permission error: {error}")

except Exception as error:
    st.exception(error)