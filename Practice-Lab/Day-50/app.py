import os
import re
import time
import json
import requests
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------- CONFIGURATION ----------------

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:4b")
OLLAMA_URL = "http://localhost:11434/api/chat"

st.set_page_config(
    page_title="Day 50 - CI/CD Pipeline Failure Investigator",
    page_icon="⚙️",
    layout="wide"
)

# ---------------- PREPACKAGED REALISTIC CI/CD FAILURE LOGS ----------------

SAMPLE_PIPELINE_RUNS = {
    "Run #4092 - Pytest Unit Test Assertion Failure": {
        "pipeline_name": "backend-core-ci",
        "branch": "feature/jwt-auth-revamp",
        "commit": "a8f3b21",
        "stages": [
            {"name": "Checkout & Setup", "status": "SUCCESS", "duration": "14s"},
            {"name": "Lint & Static Analysis", "status": "SUCCESS", "duration": "28s"},
            {"name": "Unit & Integration Tests", "status": "FAILED", "duration": "1m 12s"},
            {"name": "Docker Image Build", "status": "SKIPPED", "duration": "0s"},
            {"name": "Deploy to Staging", "status": "SKIPPED", "duration": "0s"}
        ],
        "failed_stage": "Unit & Integration Tests",
        "raw_logs": """
[2026-11-13T09:12:01Z] Running pytest with coverage...
============================= test session starts ==============================
platform linux -- Python 3.12.2, pytest-8.1.1, pluggy-1.4.0
rootdir: /home/runner/work/backend-core/backend-core
collected 42 items

tests/unit/test_health.py ....                                           [  9%]
tests/unit/test_database.py .........                                    [ 30%]
tests/unit/test_auth.py ..F......                                        [ 52%]

=================================== FAILURES ===================================
_________________________ test_auth_token_expiration __________________________

    def test_auth_token_expiration():
        client = TestClient(app)
        expired_token = create_jwt_token(payload={"sub": "user_42"}, expires_delta=-3600)
>       response = client.get("/api/v1/protected", headers={"Authorization": f"Bearer {expired_token}"})
        
tests/unit/test_auth.py:64: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

>       assert response.status_code == 401
E       AssertionError: assert 200 == 401
E        +  where 200 = <Response [200 OK]>.status_code

tests/unit/test_auth.py:67: AssertionError
----------------------------- Captured stderr call -----------------------------
WARNING:auth.middleware:Token expired signature verification was disabled in test settings!
=========================== short test summary info ============================
FAILED tests/unit/test_auth.py::test_auth_token_expiration - AssertionError: assert 200 == 401
======================== 1 failed, 41 passed in 4.82s ==========================
Error: Process completed with exit code 1.
"""
    },
    "Run #4093 - Docker Build Missing Dependency": {
        "pipeline_name": "worker-service-build",
        "branch": "main",
        "commit": "c4d190e",
        "stages": [
            {"name": "Checkout Code", "status": "SUCCESS", "duration": "10s"},
            {"name": "Security Vulnerability Scan", "status": "SUCCESS", "duration": "35s"},
            {"name": "Docker Image Build", "status": "FAILED", "duration": "48s"},
            {"name": "Push to ECR", "status": "SKIPPED", "duration": "0s"},
            {"name": "Helm Deploy EKS", "status": "SKIPPED", "duration": "0s"}
        ],
        "failed_stage": "Docker Image Build",
        "raw_logs": """
[2026-11-13T09:15:20Z] Building image worker-service:v2.4.1 ...
Step 1/10 : FROM python:3.12-slim
 ---> 9c4b78291f0c
Step 2/10 : WORKDIR /app
 ---> Using cache
 ---> 34db11fa9021
Step 3/10 : COPY requirements.txt .
 ---> Using cache
 ---> 88a101bc3340
Step 4/10 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Running in 7289d0f192b3
Collecting psycopg2-binary==2.9.9
  Downloading psycopg2_binary-2.9.9-cp312-cp312-manylinux_2_17_x86_64.whl
Collecting pyyaml==6.0.1
  Downloading PyYAML-6.0.1-cp312-cp312-linux_x86_64.whl
Installing collected packages: psycopg2-binary, pyyaml
Successfully installed psycopg2-binary-2.9.9 pyyaml-6.0.1
Step 5/10 : RUN apt-get update && apt-get install -y libpq-dev gcc
 ---> Running in e8120fa2110c
Err:1 http://deb.debian.org/debian bookworm InRelease
  Temporary failure resolving 'deb.debian.org'
W: Failed to fetch http://deb.debian.org/debian/dists/bookworm/InRelease  Temporary failure resolving 'deb.debian.org'
W: Some index files failed to download. They have been ignored, or old ones used instead.
Reading package lists...
Building dependency tree...
Reading state information...
E: Unable to locate package libpq-dev
The command '/bin/sh -c apt-get update && apt-get install -y libpq-dev gcc' returned a non-zero code: 100
Error: Docker build exited with error code 100
"""
    },
    "Run #4094 - Kubernetes / Cloud Deployment Auth Expiry": {
        "pipeline_name": "payments-deploy-prod",
        "branch": "release/v1.9.0",
        "commit": "9012fef",
        "stages": [
            {"name": "Build & Lint", "status": "SUCCESS", "duration": "45s"},
            {"name": "Automated Tests", "status": "SUCCESS", "duration": "2m 10s"},
            {"name": "Image Tagging", "status": "SUCCESS", "duration": "18s"},
            {"name": "Terraform Infrastructure", "status": "SUCCESS", "duration": "1m 30s"},
            {"name": "Kubernetes Helm Deploy", "status": "FAILED", "duration": "22s"}
        ],
        "failed_stage": "Kubernetes Helm Deploy",
        "raw_logs": """
[2026-11-13T09:20:10Z] Triggering Helm upgrade for release: payments-prod ...
[2026-11-13T09:20:12Z] Authenticating with AWS IAM OIDC Role: arn:aws:iam::123456789012:role/github-actions-eks-deployer
[2026-11-13T09:20:15Z] Refreshing kubeconfig for cluster: production-eks-cluster-ap-south-1
Traceback (most recent call last):
  File "/opt/deploy/scripts/helm_deploy.py", line 42, in assume_eks_role
    response = sts_client.assume_role_with_web_identity(
  File "/usr/local/lib/python3.12/site-packages/botocore/client.py", line 535, in _api_call
    return self._make_api_call(operation_name, kwargs)
botocore.exceptions.ClientError: An error occurred (ExpiredToken) when calling the AssumeRoleWithWebIdentity operation: The OpenID Connect security token included in the request is expired.
Error: Unable to connect to the server: Unauthorized
Error: Process exited with return code 1
"""
    }
}

# ---------------- LOG SLICER & ERROR EXTRACTOR ----------------

def extract_critical_error_segment(raw_log: str) -> dict:
    """Extracts stack traces, fatal error strings, and exit codes from noisy logs."""
    lines = raw_log.strip().split("\n")
    error_lines = []
    exit_code = "Unknown"
    culprit_file = "Unknown"

    for line in lines:
        if any(err_word in line.lower() for err_word in ["error:", "failed", "fatal:", "traceback", "assertionerror", "exit code", "exception"]):
            error_lines.append(line.strip())
        
        # Regex for exit codes
        exit_match = re.search(r"exit code:?\s*(\d+)", line, re.IGNORECASE) or re.search(r"code:?\s*(\d+)", line, re.IGNORECASE)
        if exit_match:
            exit_code = exit_match.group(1)

        # Regex for culprit file/line
        file_match = re.search(r"([\w/\.-]+\.py:\d+)", line)
        if file_match and culprit_file == "Unknown":
            culprit_file = file_match.group(1)

    # Slice the last 25 lines as the most relevant failure context
    tail_context = "\n".join(lines[-35:])

    return {
        "exit_code": exit_code,
        "culprit_file": culprit_file,
        "key_error_signals": error_lines[:8],
        "focused_failure_snippet": tail_context
    }

# ---------------- LOCAL AI ROOT CAUSE ANALYZER ----------------

def generate_ai_rca_report(run_meta: dict, error_summary: dict):
    """Invokes local Qwen3 to perform Senior SRE Root Cause Analysis and generate code fix."""
    prompt = (
        "You are an expert Senior Site Reliability Engineer (SRE) and CI/CD Diagnostics Lead. "
        "Analyze the following CI/CD pipeline failure details and generate a structured root cause investigation report.\n\n"
        f"Pipeline: {run_meta['pipeline_name']} (Branch: {run_meta['branch']})\n"
        f"Failed Stage: {run_meta['failed_stage']}\n"
        f"Exit Code: {error_summary['exit_code']}\n"
        f"Culprit File/Signal: {error_summary['culprit_file']}\n"
        f"Focused Error Log:\n```\n{error_summary['focused_failure_snippet']}\n```\n\n"
        "Please provide your analysis strictly in the following format:\n"
        "### 1. Root Cause Summary\n(State clearly in 2-3 sentences what failed and why)\n\n"
        "### 2. Culprit & Failure Classification\n(Identify category: e.g. Assertion/Logic Bug, Dockerfile/DNS Build Error, or Cloud Auth Expiry)\n\n"
        "### 3. Immediate Recommended Fix & Code Diff\n(Provide concrete git diff or shell command fix)\n\n"
        "### 4. CI/CD Hardening & Prevention\n(One concrete step to prevent this failure from reoccurring in CI/CD)"
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are an autonomous Senior SRE CI/CD Diagnostics Specialist."},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 450, "num_ctx": 2048}
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=90)
        res.raise_for_status()
        return res.json()["message"]["content"]
    except Exception:
        # Deterministic SRE Fallback Analysis
        stage = run_meta["failed_stage"]
        if "test" in stage.lower():
            return (
                "### 1. Root Cause Summary\n"
                "The test `test_auth_token_expiration` failed because the test client received an HTTP 200 OK instead of the expected 401 Unauthorized status code. "
                "The log indicates that JWT expiration signature verification was disabled in test settings.\n\n"
                "### 2. Culprit & Failure Classification\n"
                "**Category:** Unit Test Logic / Test Middleware Configuration\n"
                f"**Culprit File:** `{error_summary['culprit_file']}`\n\n"
                "### 3. Immediate Recommended Fix & Code Diff\n"
                "```diff\n"
                "--- a/config/settings.py\n"
                "+++ b/config/settings.py\n"
                "- VERIFY_JWT_EXPIRATION = False\n"
                "+ VERIFY_JWT_EXPIRATION = True\n"
                "```\n\n"
                "### 4. CI/CD Hardening & Prevention\n"
                "Add an automated config sanity test verifying that security and signature verification flags are strictly enforced in test environments."
            )
        elif "docker" in stage.lower():
            return (
                "### 1. Root Cause Summary\n"
                "The Docker image build failed during package installation (`apt-get update`) due to a DNS resolution failure resolving `deb.debian.org`, followed by failure to locate `libpq-dev`.\n\n"
                "### 2. Culprit & Failure Classification\n"
                "**Category:** Container Build / Ephemeral Network Resolution Failure\n\n"
                "### 3. Immediate Recommended Fix & Code Diff\n"
                "```diff\n"
                "--- a/Dockerfile\n"
                "+++ b/Dockerfile\n"
                "- RUN apt-get update && apt-get install -y libpq-dev gcc\n"
                "+ RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \\\n"
                "+     libpq-dev gcc && rm -rf /var/lib/apt/lists/*\n"
                "```\n\n"
                "### 4. CI/CD Hardening & Prevention\n"
                "Enable Docker BuildKit layer caching and configure fallback DNS servers (8.8.8.8) in CI runner daemon settings."
            )
        else:
            return (
                "### 1. Root Cause Summary\n"
                "The deployment pipeline failed during AWS EKS authentication because the OIDC web identity token passed by the GitHub Actions runner expired before Helm could assume the role.\n\n"
                "### 2. Culprit & Failure Classification\n"
                "**Category:** Cloud Infrastructure / OIDC Credential Expiration\n\n"
                "### 3. Immediate Recommended Fix\n"
                "Refresh the GitHub Actions `id-token: write` permission and ensure the `aws-actions/configure-aws-credentials` action duration is set to at least 1800 seconds.\n\n"
                "### 4. CI/CD Hardening & Prevention\n"
                "Implement automatic credential refresh in pre-deployment hooks before executing long-running Kubernetes manifests."
            )

# ---------------- UI DASHBOARD ----------------

st.title("⚙️ Day 50 — CI/CD Pipeline Failure Investigation Agent 🤖")
st.caption("Autonomous Log Slicing • Stage Failure Classification • Senior SRE Root Cause Analysis (Ollama Qwen3)")

# Sidebar Selection
with st.sidebar:
    st.header("📋 Pipeline Failure Selection")
    preset_choice = st.selectbox("Select Failing Pipeline Run:", list(SAMPLE_PIPELINE_RUNS.keys()))
    run_meta = SAMPLE_PIPELINE_RUNS[preset_choice]

    st.divider()
    st.markdown(f"**Pipeline:** `{run_meta['pipeline_name']}`")
    st.markdown(f"**Branch:** `{run_meta['branch']}`")
    st.markdown(f"**Commit:** `{run_meta['commit']}`")
    st.markdown(f"**Failed Stage:** ❌ `{run_meta['failed_stage']}`")

    run_rca_btn = st.button("🔍 Run Autonomous RCA Investigation", type="primary", use_container_width=True)

# Pipeline DAG Stage Flowchart Visualizer
st.subheader("🚀 CI/CD Execution Pipeline Flow")
stages = run_meta["stages"]
cols = st.columns(len(stages))

for idx, stage in enumerate(stages):
    with cols[idx]:
        if stage["status"] == "SUCCESS":
            st.success(f"**{stage['name']}**\n\n✅ {stage['duration']}")
        elif stage["status"] == "FAILED":
            st.error(f"**{stage['name']}**\n\n❌ {stage['duration']} (FAILED)")
        else:
            st.caption(f"**{stage['name']}**\n\n⚪ {stage['status']}")

st.divider()

# Error Slicing
error_data = extract_critical_error_segment(run_meta["raw_logs"])

# Tabs for Investigation
tab_rca, tab_logs, tab_signals, tab_export = st.tabs([
    "🧠 AI Root Cause Analysis (RCA)",
    "📜 Raw CI/CD Execution Logs",
    "🎯 Sliced Error Signals",
    "📄 Export Incident Post-Mortem"
])

if "current_rca" not in st.session_state or run_rca_btn:
    with st.spinner("Autonomous SRE agent analyzing stack traces, exit codes, and failure contexts..."):
        st.session_state.current_rca = generate_ai_rca_report(run_meta, error_data)

with tab_rca:
    st.subheader("Senior SRE Incident Diagnostic Report")
    st.markdown(st.session_state.current_rca)

with tab_logs:
    st.subheader("Raw Terminal / Build Logs")
    st.code(run_meta["raw_logs"].strip(), language="text")

with tab_signals:
    st.subheader("Extracted Error Signatures")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Exit Code", error_data["exit_code"])
        st.metric("Culprit Reference", error_data["culprit_file"])
    with c2:
        st.write("**Discovered Error Indicators:**")
        for sig in error_data["key_error_signals"]:
            st.markdown(f"- `{sig}`")

    st.write("**Focused Failure Snippet (Last 35 Lines):**")
    st.code(error_data["focused_failure_snippet"], language="text")

with tab_export:
    st.subheader("Downloadable Post-Mortem Incident Report")
    incident_export = {
        "incident_id": f"INC-{preset_choice.split()[1]}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pipeline": run_meta["pipeline_name"],
        "branch": run_meta["branch"],
        "commit": run_meta["commit"],
        "failed_stage": run_meta["failed_stage"],
        "exit_code": error_data["exit_code"],
        "culprit_reference": error_data["culprit_file"],
        "root_cause_analysis": st.session_state.current_rca
    }
    st.download_button(
        "📥 Download Post-Mortem Incident Report (JSON)",
        data=json.dumps(incident_export, indent=2),
        file_name=f"post_mortem_{run_meta['pipeline_name']}.json",
        mime="application/json",
        use_container_width=True
    )

