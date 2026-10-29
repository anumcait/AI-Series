# 🚀 Day 37 — Build a Local AI Task Queue & Background Job Processing System ⚙️🤖

## Objective

Build a local AI application using Python, Streamlit, Ollama, Qwen3, and SQLite to accept multiple AI tasks, process them in the background, track job status, retry failures, and monitor execution through a dashboard.

## 1\. Project Setup

- Created the `Day-37` project folder in VS Code.
- Created and activated a Python virtual environment.
- Installed dependencies:bash
  ```
  pip install streamlit requests
  ```
- Installed Ollama and verified that the local service was running.
- Verified the installed Qwen3 model.

## 2\. Model Configuration

The model used for this project is:

python

```
MODEL = "qwen3:4b"
```

The application sends AI requests to Ollama's local generation API.

## 3\. Application Implementation

Created `app.py` containing:

- Streamlit interface for submitting AI tasks.
- Support for summarization, translation, and question answering.
- Unique UUID assigned to every submitted job.
- SQLite database (`jobs.db`) for persistent job records.
- Background worker using Python threading.
- Job status tracking: `Pending`, `Running`, `Completed`, and `Failed`.
- Priority scheduling for High and Normal jobs.
- Retry mechanism with a maximum of three attempts.
- Automatic recovery of interrupted Running jobs during application startup.
- Dashboard metrics for pending, running, completed, and failed jobs.
- Success rate, job history, timestamps, attempt counts, results, errors, and execution duration.
- Automatic dashboard refresh every three seconds.

## 4\. Run the Application

Start the application from the `Day-37` directory:

bash

```
python -m streamlit run app.py
```

Open the local address:

text

```
http://localhost:8501
```

The dashboard allows users to submit AI tasks, view their unique job IDs, monitor progress, and retrieve completed results.

## 5\. Practical Tests Completed

- Submitted a summarization task and received a concise summary.
- Submitted a French translation task and received an English translation.
- Submitted a question-answering task about SQLite and verified the model's response.
- Confirmed that all three jobs received unique IDs.
- Observed three completed jobs with zero pending and zero failed jobs.
- Verified a dashboard success rate of 100%.
- Observed job attempt counts, timestamps, and execution durations.
- Confirmed that some tasks required multiple attempts.

### Observed Results

- Total completed jobs: 3
- Pending jobs: 0
- Running jobs: 0
- Failed jobs: 0
- Success rate: 100%
- Last-attempt durations: 35, 271, and 74 seconds.

## 6\. Additional Tests to Complete

1. Restart Streamlit and verify that previous jobs and results remain available in SQLite.
2. Queue multiple jobs and confirm that High-priority pending jobs are processed before Normal-priority pending jobs.
3. Stop Ollama temporarily and verify that eligible failed jobs are retried.
4. Confirm that jobs transition to `Failed` after three unsuccessful attempts.
5. Verify that dashboard metrics and execution times update correctly.

## 7\. Project Files

- `app.py` — Application, background worker, and dashboard.
- `jobs.db` — Persistent job records and results, created automatically.
- `.venv/` — Python virtual environment.
- `day.md` — Project notes and documentation.

## Key Learning

Background workers allow AI tasks to execute independently of the user interface. SQLite preserves job history, priority scheduling manages queued workloads, retry handling helps recover from temporary failures, and the Streamlit dashboard makes task progress and results easy to monitor.

**Status:** Core implementation and three AI task tests completed successfully. Persistence across restart, priority ordering under a backlog, and failure recovery remain to be verified.

### Screenshots

