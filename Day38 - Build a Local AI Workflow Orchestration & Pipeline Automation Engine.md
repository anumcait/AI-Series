# 🚀 Day 38 — Build a Local AI Workflow Orchestration & Pipeline Automation Engine ⚙️🤖

## 1. Project Objective

Build a local AI workflow engine that connects multiple AI tasks, manages dependencies, supports conditional branching, executes independent tasks in parallel, handles failures and stores workflow history.

**Technology Stack:**
- Python – Workflow engine
- Ollama + Qwen3 – Local AI execution
- NetworkX – Dependency graph
- Threading – Background execution
- SQLite – Workflow history
- Streamlit – Monitoring dashboard
- Plotly – Pipeline visualization

## 2. Project Setup

Create the project directory:

```bash
mkdir day38_workflow_engine
cd day38_workflow_engine
python -m venv venv
```

Activate the virtual environment:

Windows:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

Create `requirements.txt`:

```text
streamlit
ollama
networkx
plotly
pandas
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Ollama from https://ollama.com/download.

Download Qwen3:

```bash
ollama pull qwen3:8b
```

Verify installation:

```bash
ollama list
```

## 3. Workflow Architecture

Customer support ticket processing follows this execution sequence:

1. Classification – Identify ticket category and priority.
2. Issue Analysis – Extract important issue details.
3. Sentiment Analysis – Identify customer sentiment and urgency.
4. Decision – Select the appropriate processing branch.
5. Response Generation – Generate urgent or standard response.
6. Storage – Save results and execution history in SQLite.

**Dependencies:**
- Classification runs first.
- Issue analysis and sentiment analysis execute in parallel.
- Decision waits for both analysis tasks.
- Only the selected response branch executes.

## 4. Application Implementation

Create `app.py`.

The application contains:

- SQLite database initialization and storage.
- Reusable task definitions and dependencies.
- NetworkX directed acyclic graph.
- Ollama integration for Qwen3.
- Background workflow execution.
- Parallel task scheduling.
- Conditional branching based on classification.
- Three-attempt failure retry mechanism.
- Dependency failure handling.
- Streamlit monitoring dashboard.
- Plotly workflow visualization.
- Persistent workflow history.

The workflow execution statuses are:

| Status | Description |
|---|---|
| Pending | Waiting for dependencies |
| Running | Task executing |
| Completed | Task successfully finished |
| Failed | Task failed after retries |
| Skipped | Conditional branch not selected |
| Blocked | Dependency failure prevented execution |

## 5. Run the Application

Start Ollama if it is not already running:

```bash
ollama serve
```

Open another terminal and execute:

```bash
streamlit run app.py
```

Open:

http://localhost:8501

Enter a customer support ticket and click **Start Workflow**.

Observe task execution and the live pipeline visualization.

## 6. Practical Testing

### Test 1 – Task Dependencies

Submit:

"My payment was deducted, but my order is still unpaid."

Verify classification completes before analysis and sentiment tasks begin.

### Test 2 – Conditional Branching

Submit an urgent payment complaint.

Verify:
- Urgent response executes.
- Standard response is skipped.

Submit a normal customer enquiry.

Verify:
- Standard response executes.
- Urgent response is skipped.

### Test 3 – Parallel Execution

Verify issue analysis and sentiment analysis run simultaneously after classification.

### Test 4 – Failure Handling

Temporarily modify `ask_ai()` to raise an exception.

Verify:
- Three execution attempts occur.
- Failed task becomes Failed.
- Unfinished tasks become Blocked.
- Workflow becomes Failed.

Restore the original function after testing.

### Test 5 – SQLite History

Verify `workflow.db` contains:

- `runs` – Workflow execution information.
- `tasks` – Task statuses, outputs, errors and retry attempts.

### Test 6 – Restart Recovery

Stop Streamlit and restart it.

Verify previous workflow executions and results remain available in the dashboard.

## 7. Real-Time Execution

The workflow engine executes tasks in background threads.

After each task execution, its status and output are saved in SQLite.

Streamlit periodically refreshes the dashboard and retrieves updated task statuses.

This provides polling-based live workflow monitoring.

## 8. Final Project Structure

```text
day38_workflow_engine/
│
├── venv/
├── app.py
├── requirements.txt
└── workflow.db
```

## 9. Day 38 Learning Outcomes

- Workflow orchestration.
- Directed Acyclic Graphs (DAGs).
- Task dependency management.
- Sequential and parallel execution.
- Conditional branching.
- Background task processing.
- Automatic retry and failure handling.
- SQLite execution history.
- Real-time workflow monitoring.
- Visual pipeline representation.

## 10. Day 38 Conclusion

Successfully built a local AI workflow orchestration engine using Python, Ollama and Qwen3.

The application connects multiple AI tasks into an automated workflow, manages dependencies, executes independent tasks concurrently, selects conditional execution paths, handles failures and stores execution history.

**Key Takeaway:** Individual AI tasks perform useful operations. Workflow orchestration connects those tasks into complete, intelligent and automated business processes.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/7f328ed9-e2bc-48b2-91b3-48b57d6906d0" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/1769520c-d8b8-4934-9cc2-06862ddd8ab9" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/774b3779-eb72-4ce1-9d50-717e2ce16e19" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/dbf12d40-1c69-4d6c-b984-cfaf4f113610" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/b4a3efe9-9a0b-4f5b-b472-ad0225e4befd" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/272268a7-3d10-4a66-8036-421648d679dd" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/288505ea-19a8-4966-9679-77c2318582c2" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/238ffcef-c731-4300-b037-1b98e41a0fce" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/3c83faa8-d0e1-4804-9114-762ed66bde7c" />









