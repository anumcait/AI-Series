# Day 41 — Local AI Infrastructure Anomaly Detection & Predictive Alerting System

## Overview

Built a local AI-powered infrastructure monitoring application using Python, Ollama, Qwen3, Streamlit, and SQLite.

The application continuously monitors system resources, detects unusual behaviour, records alerts, and uses a local AI model to explain potential infrastructure problems.

## Objective

- Monitor CPU, memory, disk, and network usage.
- Detect infrastructure anomalies.
- Identify potential resource-related risks.
- Generate AI-powered explanations.
- Maintain historical monitoring data.
- Visualize infrastructure health through a dashboard.

## Technology Stack

- Python — Core application
- psutil — System metric collection
- Ollama — Local LLM execution
- Qwen3 — AI-powered investigation
- Streamlit — Monitoring dashboard
- SQLite — Persistent storage
- Pandas — Data processing
- NumPy — Statistical calculations
- Scikit-learn — Isolation Forest anomaly detection
- Plotly — Interactive charts
- Threading — Background metric collection

## Project Structure

    day41-ai-monitor/
    ├── app.py
    ├── requirements.txt
    ├── monitoring.db
    └── venv/

The SQLite database is generated automatically when the application starts.

## How It Works

    System Metrics
          |
          v
    Metric Collection
          |
          v
    SQLite Storage
          |
          v
    Anomaly Detection
          |
          v
    Risk Identification
          |
          v
    AI Investigation
          |
          v
    Recommendations
          |
          v
    Streamlit Dashboard

### 1. Metric Collection

Uses `psutil` to collect:

- CPU utilization
- Memory utilization
- Disk utilization
- Network receive speed
- Network send speed

Metrics are collected approximately every 3 seconds.

### 2. Anomaly Detection

Three detection approaches are implemented:

- **Threshold Detection:** Identifies resource usage above configured limits.
- **Statistical Detection:** Uses Z-scores to identify unusual deviations from recent measurements.
- **Isolation Forest:** Identifies unusual combinations of infrastructure metrics using machine learning.

Default thresholds:

| Metric | Warning Threshold |
|---|---:|
| CPU | 85% |
| Memory | 85% |
| Disk | 90% |

Values reaching 95% or above are classified as critical by the threshold detector.

### 3. Background Monitoring

A Python background thread continuously collects infrastructure metrics and records them in SQLite.

The dashboard refreshes independently every 3 seconds to display updated measurements.

### 4. AI Investigation

Ollama runs Qwen3 locally.

When the user clicks the AI investigation button, the application sends the latest measurements and recent alerts to the model.

The AI provides:

- Infrastructure condition
- Supporting metric evidence
- Possible explanations
- Investigation steps
- Recommended corrective actions

AI-generated explanations are hypotheses and do not confirm root causes.

### 5. Historical Storage

SQLite maintains two tables:

- `metrics` — Timestamped infrastructure measurements.
- `alerts` — Detected anomalies, severity, metric values, and reasons.

Historical records remain available after restarting the application.

### 6. Dashboard

The Streamlit dashboard displays:

- Current CPU, memory, and disk usage.
- Network receive rate.
- Infrastructure performance charts.
- Recent anomaly records.
- Disk capacity trend estimate.
- AI-powered investigation.
- CSV export for metrics and alerts.

## Installation and Execution

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```
.\venv\Scripts\Activate.ps1
```

Linux / macOS:

```
source venv/bin/activate
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Download Local AI Model

```
ollama pull qwen3:4b
```

### Start Application

```
streamlit run app.py
```

Open:

[http://localhost:8501](http://localhost:8501?utm_source=chatgpt.com)

## Practical Testing

1. Start the application and observe live CPU, memory, disk, and network metrics.
2. Temporarily reduce the CPU threshold to trigger a test warning.
3. Restore the original thresholds.
4. Allow at least 50 measurements to be collected to activate Isolation Forest detection.
5. Click the AI investigation button and verify the Qwen3 response.
6. Restart the application and verify that historical records remain available.
7. Download the metrics and alert CSV files.

## Key Learning

- Real-time infrastructure metric collection
- Linux and system resource monitoring concepts
- Threshold-based alerting
- Statistical anomaly detection
- Machine learning with Isolation Forest
- Infrastructure trend analysis
- Predictive capacity estimation
- Local LLM integration using Ollama
- AI-powered operational investigation
- SQLite persistence
- Streamlit monitoring dashboards

## Important Limitations

- The current implementation monitors the local machine only.
- Network measurements represent machine-level traffic.
- Alerts are stored locally; external notification integrations are not implemented.
- Disk capacity estimates assume the recent growth rate continues.
- Anomaly detection identifies unusual behaviour but does not guarantee that a failure will occur.
- AI recommendations require human evaluation; infrastructure changes are not executed automatically.

## Day 41 Outcome

Successfully built a local infrastructure monitoring prototype that collects real system metrics, detects unusual behaviour using configurable thresholds and machine learning, stores historical data, and uses Qwen3 to explain potential infrastructure risks.

Key Takeaway: Intelligent monitoring combines infrastructure metrics, anomaly detection, and AI-powered analysis to help engineers identify potential problems earlier and make better operational decisions.

```
