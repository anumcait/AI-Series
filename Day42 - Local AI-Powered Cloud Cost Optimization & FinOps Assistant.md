# 🚀 Day 42 — Local AI-Powered Cloud Cost Optimization & FinOps Assistant

## Objective

Build a local AI-powered AWS FinOps assistant using Python, Ollama, Qwen3, Streamlit, SQLite, Boto3, Pandas, and Plotly to analyze cloud costs, identify potentially idle resources, detect cost spikes, and generate AI-powered cost optimization recommendations.

## Tech Stack

- Python
- Ollama + Qwen3
- AWS Boto3
- AWS Cost Explorer
- AWS EC2
- AWS CloudWatch
- AWS EBS
- Streamlit
- SQLite
- Pandas
- Plotly

## Project Structure

```text
day42-finops-assistant/
│
├── app.py
├── requirements.txt
├── finops.db
└── venv/
```

## Implementation

### 1. Environment Setup

Created a Python virtual environment and installed the required packages.

Dependencies:
- streamlit
- streamlit-autorefresh
- boto3
- pandas
- plotly
- requests

### 2. Local AI Setup

Installed Ollama and downloaded the Qwen3 model.

```powershell
ollama pull qwen3:4b
```

Used the local Ollama API to generate cloud cost analysis and recommendations.

### 3. AWS Configuration

Configured an AWS CLI profile named `day42` and verified the connection using:

```powershell
aws sts get-caller-identity
```

Configured read-only IAM permissions for:
- AWS Cost Explorer
- EC2 instance inventory
- EBS volume inventory
- CloudWatch CPU metrics

### 4. AWS Cost Collection

Used Boto3 and AWS Cost Explorer to retrieve available daily AWS costs grouped by service.

Configured the application to collect the last **60 days** of cost data.

### 5. Infrastructure Monitoring

Collected EC2 instance information, including:
- Instance ID and name
- Instance type
- Instance state
- Average CPU utilization over seven days

Retrieved EBS volume information and identified unattached volumes.

### 6. Cost Analysis

Implemented basic FinOps analysis:

- Total cost over the selected 60-day period
- Estimated 30-day spending based on average daily cost
- Service-wise cost breakdown
- Daily spending trends
- Cost spike detection using the preceding seven-day average

### 7. Resource Optimization Detection

Implemented rule-based checks to identify:

- Potentially idle running EC2 instances using average CPU below 5%
- Unattached EBS volumes
- Unusual daily cost increases

These findings are recommendations for investigation, not automatic resource changes.

### 8. Local AI Analysis

Integrated Ollama with Qwen3 to analyze AWS cost and resource findings.

The AI provides:
- Cost summaries
- Possible reasons for unusual spending
- Resource investigation suggestions
- Cost optimization recommendations
- Validation steps before taking action

### 9. SQLite Storage

Created a local SQLite database named `finops.db`.

Stored monitoring snapshots containing:
- Collection timestamp
- Total cost
- Potentially idle EC2 count
- Unattached EBS count
- Estimated monthly spending

### 10. Streamlit Dashboard

Built an interactive dashboard displaying:

- Last 60-day AWS cost
- Estimated 30-day spending
- Potentially idle EC2 count
- Unattached EBS count
- Daily cost chart
- Service-wise cost chart
- EC2 and EBS inventory
- Cost optimization findings
- Qwen3 AI analysis
- Monitoring history

Added automatic dashboard refresh every five minutes and manual refresh functionality.

### 11. CSV Export

Implemented CSV downloads for:
- AWS cost data
- Cost optimization findings

## How the Workflow Works

AWS Account → Cost Explorer / EC2 / EBS / CloudWatch → Python Data Collection → Cost Analysis → Resource Detection → Qwen3 AI Analysis → SQLite Storage → Streamlit Dashboard

## Important Project Notes

- AWS billing data is periodically updated and is not instant.
- The dashboard refreshes every five minutes.
- EC2 and EBS inventory is collected from the configured AWS region.
- Cost Explorer retrieves account-level billing data.
- CPU analysis uses the previous seven days of available CloudWatch metrics.
- Monthly spending is an estimate, not an AWS billing forecast.
- No resources are automatically stopped, resized, or deleted.
- All AI recommendations require human validation.

## Day 42 Outcome

Built a local AI-powered AWS FinOps assistant that collects cloud billing and infrastructure data, identifies potential cost optimization opportunities, detects unusual spending, generates Qwen3 recommendations, stores monitoring history, and displays findings through an interactive Streamlit dashboard.

**Key Learning:** Cloud cost optimization combines billing analysis, infrastructure monitoring, resource utilization, anomaly detection, and AI-assisted decision-making.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/a673a5c2-9d00-4d7e-aa22-3ba481df7a51" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/b1411ee7-c3b9-40ea-83a1-2d7eb2db5855" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/43cf15ac-01fa-457e-834a-9954bfd10081" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/6e1de7d0-6c23-486c-bad3-37a069b6108c" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/079210ec-c926-4b81-903b-0dcc917e6dd1" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/d43b0c7c-6e2f-4e3c-892a-3ae97bedf769" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/ae4ece5e-7f57-4703-a8a9-a30fb6869b09" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/4cfb6a54-7a3c-4bdf-9896-55787c7deda1" />








