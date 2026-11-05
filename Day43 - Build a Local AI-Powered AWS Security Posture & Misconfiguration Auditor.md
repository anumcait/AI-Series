 # 🚀 Day 43 — Build a Local AI-Powered AWS Security Posture & Misconfiguration Auditor 🔐☁️

## Objective
Built a local AI-powered AWS security auditing application using Python, Boto3, Ollama, Qwen3, and Streamlit to identify common AWS security misconfigurations, classify risks, and generate AI-powered remediation recommendations.

## Tech Stack
- Python
- AWS Boto3
- AWS IAM, S3, EC2, EBS, RDS, CloudTrail
- Ollama and Qwen3
- Streamlit
- SQLite
- Pandas and Plotly

## Implementation
- Configured AWS CLI using a dedicated read-only IAM profile.
- Connected Python to AWS using Boto3.
- Implemented security checks for S3 public access, EC2 security group rules, unencrypted EBS volumes, publicly accessible RDS databases, IAM access-key age, missing MFA, and CloudTrail logging status.
- Classified detected findings by severity: Critical, High, and Medium.
- Stored audit findings and timestamps in SQLite.
- Integrated local Qwen3 through Ollama to explain security findings and suggest remediation steps.
- Created a Streamlit dashboard to display findings, severity charts, scan errors, and audit history.
- Added CSV export for security findings.

## Workflow
AWS Account → Boto3 Resource Discovery → Security Configuration Checks → Risk Classification → SQLite Storage → Qwen3 Analysis → Streamlit Dashboard

## Important Notes
- AWS checks use read-only permissions; no resources are modified.
- S3 and IAM checks are account-wide, while EC2, EBS, RDS, and CloudTrail checks use the selected region.
- Audits run on demand, not continuously.
- Incomplete checks caused by permission errors must not be treated as successful security checks.
- AI recommendations require human review before implementation.

## Outcome
Created a local AWS security auditing tool that combines cloud configuration checks, security risk identification, local AI analysis, audit history, and an interactive dashboard.