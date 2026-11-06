# 🚀 Day 44 — Build a Local AI-Powered AWS Security Incident Detection & Investigation Assistant 🔐☁️

## Objective
Build a local AI-powered application to collect AWS CloudTrail events, detect suspicious activities, and investigate potential security incidents using local Qwen3.

## Technologies Used
- Python, Boto3, AWS CloudTrail
- Ollama – Qwen3
- Streamlit
- SQLite
- Pandas, Plotly

## Work Completed

1. **CloudTrail Integration**
   - Connected to AWS using the `day44` profile.
   - Collected recent management events from `ap-south-1`.
   - Implemented periodic polling using a 60-second refresh.

2. **Security Event Detection**
   - Detected failed console login attempts.
   - Identified `AccessDenied` and `UnauthorizedOperation` errors.
   - Monitored selected IAM, security group, CloudTrail, EC2, and RDS changes.
   - Classified events by severity.

3. **Repeated Denial Detection**
   - Checked denied API activity within a 10-minute window.
   - Flagged users or source IPs with five or more denied events.

4. **SQLite Storage**
   - Stored collected CloudTrail events.
   - Used event IDs to prevent duplicate records.

5. **Local AI Investigation**
   - Integrated Ollama with Qwen3.
   - Generated explanations and investigation recommendations from collected events.

6. **Streamlit Dashboard**
   - Added automatic polling and a manual scan option.
   - Displayed AWS account details, event history, severity counts, and suspicious activity.
   - Added charts and CSV export.

## Workflow

CloudTrail → Event Collection → Rule-Based Detection → Severity Classification → Qwen3 Investigation → SQLite → Streamlit Dashboard

## Important Limitations
- CloudTrail events may take several minutes to appear.
- The application uses polling, not real-time streaming.
- Detection covers management events in the selected region.
- Findings require human investigation.
- No automatic AWS resource changes or remediation.

## Outcome
Built a local AWS security incident detection and investigation assistant using Python, Boto3, CloudTrail, Ollama, Qwen3, Streamlit, and SQLite.

### Screenshots
