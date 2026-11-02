# Day 40 — AI-Powered DevOps Incident Response & Root Cause Analysis

## 1\. Project Objective

Build a local AI-powered DevOps incident management system using Python, Ollama, Qwen3, Streamlit and SQLite.

The system analyzes application/server logs, detects errors, classifies incidents, uses multiple AI agents for investigation, generates root cause reports and recommends corrective actions.

## 2\. Technology Stack

- Python – Core application
- Ollama + Qwen3 – Local AI analysis
- Streamlit – Web dashboard
- SQLite – Incident storage
- Pandas – Log processing
- Regex – Error detection
- Pydantic – Structured reports
- Plotly – Dashboard visualization
- ThreadPoolExecutor – Parallel AI agents

## 3\. Install Prerequisites

Install Python 3.10+, Ollama and Qwen3.

bash

```bash
ollama pull qwen3:4b
ollama list
ollama serve
```

Verify Ollama:

bash

```bash
curl http://localhost:11434/api/tags
```

## 4\. Create Project Structure

text

```text
day40-aiops/
│
├── app.py
├── requirements.txt
├── incidents.db
│
├── logs/
│   ├── tomcat.log
│   ├── mysql.log
│   ├── infrastructure.log
│   ├── deployment.log
│   └── network.log
│
└── reports/
```

Create the project:

bash

```bash
mkdir day40-aiops
cd day40-aiops
python -m venv venv
```

Activate virtual environment:

Windows:

powershell

```powershell
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

bash

```bash
source venv/bin/activate
```

## 5\. Install Python Libraries

Create `requirements.txt`:

text

```text
streamlit
ollama
pandas
plotly
pydantic
```

Install:

bash

```bash
pip install -r requirements.txt
```

## 6\. Create Sample Log Files

Create the following five files inside the `logs` folder.

### tomcat.log

text

```text
2026-11-02 09:00:01 INFO Tomcat server started
2026-11-02 09:01:10 INFO Application deployed
2026-11-02 09:02:15 ERROR HTTP 500 Internal Server Error
2026-11-02 09:02:16 ERROR NullPointerException at UserController.java:45
2026-11-02 09:02:18 ERROR HTTP 500 Internal Server Error
2026-11-02 09:02:20 ERROR NullPointerException at UserController.java:45
2026-11-02 09:02:25 CRITICAL Application request processing failed
```

Expected: Application failure.

### mysql.log

text

```text
2026-11-02 09:10:01 INFO Database connection initialized
2026-11-02 09:11:01 ERROR Communications link failure
2026-11-02 09:11:02 ERROR Connection refused: mysql:3306
2026-11-02 09:11:05 ERROR Unable to acquire database connection
2026-11-02 09:11:10 CRITICAL Database connection pool exhausted
```

Expected: Database connection failure.

### infrastructure.log

text

```text
2026-11-02 09:20:01 INFO CPU utilization 35%
2026-11-02 09:21:01 WARNING CPU utilization 88%
2026-11-02 09:22:01 WARNING Memory utilization 92%
2026-11-02 09:23:01 CRITICAL CPU utilization 98%
2026-11-02 09:23:05 ERROR Application response time exceeded threshold
```

Expected: High CPU and memory utilization.

### deployment.log

text

```text
2026-11-02 09:30:01 INFO Deployment started version 2.0
2026-11-02 09:30:10 INFO Previous version stopped
2026-11-02 09:30:20 ERROR Application startup failed
2026-11-02 09:30:21 ERROR Missing configuration property DATABASE_URL
2026-11-02 09:30:25 CRITICAL Application failed to initialize
```

Expected: Deployment failure.

### network.log

text

```text
2026-11-02 09:40:01 INFO API service started
2026-11-02 09:41:01 WARNING API response delayed
2026-11-02 09:41:10 ERROR Connection timed out
2026-11-02 09:41:15 ERROR Upstream service unavailable
2026-11-02 09:41:20 CRITICAL Multiple API requests failed
```

Expected: Network/API failure.

## 7\. Create Main Application

Create `app.py` and paste the complete Python application provided in the Day 40 implementation.

The application contains:

- Error detection using Regex.
- Incident severity and category classification.
- Log Analyst AI agent.
- Pattern Analyst AI agent.
- Impact Analyst AI agent.
- Parallel execution using ThreadPoolExecutor.
- Root Cause Analysis using Qwen3.
- Remediation recommendations.
- Pydantic report validation.
- SQLite incident storage.
- Streamlit dashboard.
- Live log file monitoring.
- Incident history and status tracking.
- JSON report download.

The three AI agents investigate independently. Their findings are combined by the RCA stage to generate the final incident report.

## 8\. Start the Application

First verify Ollama:

bash

```bash
ollama list
```

Test Qwen3:

bash

```bash
ollama run qwen3:8b
```

Ask:

text

```text
Explain what an HTTP 500 error means.
```

Exit using:

text

```text
/bye
```

Start Streamlit:

bash

```bash
streamlit run app.py
```

Open the browser:

text

```text
http://localhost:8501
```

## 9\. Upload and Investigate Log Files

Open the **Log Analysis** tab.

Perform the following steps:

1. Click Choose a log file.
2. Navigate to the `day40-aiops/logs/` folder.
3. Select `tomcat.log`.
4. Review the uploaded log contents.
5. Click Investigate Incident.
6. Wait for the AI agents to complete their analysis.

The system:

- Reads the uploaded log.
- Detects errors and exceptions.
- Classifies severity and incident category.
- Runs three AI agents concurrently.
- Generates possible root causes.
- Identifies supporting log evidence.
- Recommends corrective actions.
- Saves the investigation in SQLite.

Repeat the same process for:

- mysql.log
- infrastructure.log
- deployment.log
- network.log

Upload and investigate one file at a time.

## 10\. Enable Live Log Monitoring

Open the **Live Monitoring** tab.

Enter:

text

```text
logs/tomcat.log
```

Click Start / Reset Monitoring.

Open another terminal and append a new log entry.

Linux/macOS:

bash

```bash
echo "2026-11-02 10:00:00 ERROR New HTTP 500 error detected" >> logs/tomcat.log
```

Windows PowerShell:

powershell

```powershell
Add-Content logs/tomcat.log "2026-11-02 10:00:00 ERROR New HTTP 500 error detected"
```

Return to the browser.

Within approximately five seconds, the new error should appear.

Click Investigate Live Events to run the AI investigation.

Live monitoring checks for newly appended log entries every five seconds. AI analysis is started manually.

## 11\. Check Incident Dashboard

Open the **Dashboard** tab.

Verify:

- Total incidents.
- Open incidents.
- Resolved incidents.
- Severity distribution.
- Incident categories.
- Recent incident records.

Open the **Incident History** tab.

Review the stored incident details.

Test:

- Approve recommendations.
- Mark incident as resolved.

These actions update the incident status only. They do not execute infrastructure commands.

## 12\. Download Incident Report

Return to Log Analysis.

Click Download Incident Report.

Save the generated JSON report.

The report contains the AI-generated incident investigation information.

## 13\. Verify SQLite Storage

Run:

bash

```bash
python -c "import sqlite3; c=sqlite3.connect('incidents.db'); print(c.execute('SELECT id,severity,category,status FROM incidents').fetchall())"
```

Verify that your incidents are stored.

## 14\. Expected Project Outcome

| Test Scenario | Expected Detection |
| --- | --- |
| Tomcat | HTTP 500 application failure |
| MySQL | Database connection failure |
| Infrastructure | High CPU/memory |
| Deployment | Application startup failure |
| Network | API connection timeout |

The completed application should demonstrate:

- Local Qwen3 AI analysis.
- Log file upload.
- Error detection and classification.
- Three parallel AI agents.
- Root cause analysis.
- Evidence-based recommendations.
- Human approval tracking.
- SQLite incident history.
- Live file monitoring.
- Streamlit dashboard.
- Downloadable JSON reports.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/df019423-751c-4384-a54a-0adab39ed506" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/39bf80d6-a342-4176-8589-832deb870532" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/d0954db5-5d73-44ce-977e-26e74f22ca54" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/cb071ead-5813-4733-bb0c-4c22a11064a9" />




