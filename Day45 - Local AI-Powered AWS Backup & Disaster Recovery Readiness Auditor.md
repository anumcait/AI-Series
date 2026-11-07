# 🚀 Day 45 — Local AI-Powered AWS Backup & Disaster Recovery Readiness Auditor 💾☁️

## Objective

Build a local AI-powered AWS backup auditing application to inspect backup configurations, identify potential backup risks, and generate investigation recommendations using local Qwen3.

## Technologies Used

- Python
- AWS Boto3
- AWS EC2, EBS, RDS and AWS Backup
- Ollama – Qwen3
- Streamlit
- SQLite
- Pandas
- Plotly

## Work Completed

1. **AWS Integration**
   - Connected to AWS using the `day45` CLI profile.
   - Verified AWS account access using STS.
   - Configured the audit region as `ap-south-1`.

2. **Backup Resource Discovery**
   - Implemented EBS volume and snapshot discovery.
   - Added RDS database backup retention checks.
   - Implemented AWS Backup plan and vault discovery.
   - Added recovery point collection.

3. **Backup Risk Assessment**
   - Checked EBS snapshot availability and age.
   - Classified missing snapshots as High risk.
   - Identified outdated snapshots.
   - Checked RDS automated backup retention.
   - Identified databases with automated backups disabled.
   - Checked backup vault recovery point availability.

4. **SQLite Storage**
   - Created a local SQLite database.
   - Implemented storage of audit timestamps, account details, resource information, and findings.

5. **Local AI Integration**
   - Integrated Ollama with Qwen3.
   - Added AI-powered explanations and backup investigation recommendations.
   - Kept AWS auditing read-only.

6. **Streamlit Dashboard**
   - Displayed AWS account and region information.
   - Added resource discovery metrics.
   - Added backup health overview and risk visualization.
   - Added AI investigation section.
   - Implemented audit history and CSV export.
   - Added manual scanning and optional five-minute automatic polling.

## Workflow

AWS Account → Backup Resource Discovery → Configuration Checks → Risk Classification → Qwen3 Analysis → SQLite Storage → Streamlit Dashboard

## Initial Audit Result

- AWS Account: `888577063211`
- Region: `ap-south-1`
- EBS Volumes: 0
- Snapshots: 0
- RDS Databases: 0
- AWS Backup Plans: 0
- Backup Vaults: 0

AWS account connectivity was verified, but no backup resources were returned during the initial audit. Further CLI verification is required to confirm resource availability and permissions.

## Important Limitations

- Auditing is limited to the configured AWS region.
- The application uses periodic polling, not real-time event streaming.
- Backup presence does not guarantee successful recovery.
- Actual restore testing is required to validate recovery readiness.
- No automatic backup creation, deletion, restoration, or AWS configuration changes are performed.

## Outcome

Implemented a local AWS Backup & Disaster Recovery Readiness Auditor with Boto3 resource discovery, backup risk checks, SQLite storage, local Qwen3 integration, and a Streamlit dashboard.