# Day 39 — Local AI Multi-Agent Collaboration & Task Delegation System

**Technologies:** Python, Ollama, Qwen3, Streamlit, SQLite, Pydantic, NetworkX, ThreadPoolExecutor

## 1\. Project Objective

Build a local multi-agent AI system where specialized agents collaborate to complete user tasks.

The system includes:

- Coordinator Agent – Creates and delegates tasks.
- Research Agent – Collects relevant information.
- Analysis Agent – Examines problems and identifies risks.
- Execution Agent – Prepares implementation steps.
- Reviewer Agent – Evaluates results and requests revisions when necessary.

## 2\. Project Architecture

text

```text
User Request
     |
     v
Coordinator Agent
     |
     v
Task Delegation
     |
     +----------+----------+
     |          |          |
     v          v          v
 Research   Analysis   Execution
  Agent      Agent      Agent
     |          |          |
     +----------+----------+
                |
                v
          Shared Results
                |
                v
          Reviewer Agent
                |
           PASS / REVISE
                |
                v
           Final Result
                |
                v
           SQLite Storage
                |
                v
         Streamlit Dashboard
```

## 3\. Prerequisites

Install:

- Python 3.11 or newer
- Visual Studio Code
- Ollama

Download Qwen3:

bash

```bash
ollama pull qwen3:8b
```

Verify:

bash

```bash
python --version
ollama --version
ollama list
```

## 4\. Project Setup

Create the project folder:

bash

```bash
mkdir Day39_MultiAgent_System
cd Day39_MultiAgent_System
```

Create and activate a virtual environment:

bash

```bash
python -m venv venv
```

Windows:

bash

```bash
venv\Scripts\activate
```

Linux/macOS:

bash

```bash
source venv/bin/activate
```

## 5\. Project Structure

text

```text
Day39_MultiAgent_System/
│
├── app.py
├── requirements.txt
├── agents.db
└── venv/
```

`agents.db` is automatically created when the application starts.

## 6\. Dependencies

Create `requirements.txt`:

text

```text
ollama
streamlit
pydantic
networkx
pandas
plotly
```

Install:

bash

```bash
pip install -r requirements.txt
```

## 7\. Application Implementation

Create `app.py` containing the following components:

1. Configuration – Defines the Ollama model, database and agent instructions.
2. Pydantic Models – Defines structured task plans and reviewer responses.
3. SQLite Database – Creates execution and workflow history tables.
4. AI Helper – Sends prompts to the local Ollama model.
5. Coordinator – Generates and validates three specialist tasks.
6. Specialist Agents – Research, analysis and execution agents.
7. Parallel Processing – Uses ThreadPoolExecutor to execute independent tasks.
8. Shared Context – Passes completed agent outputs to dependent agents.
9. Reviewer – Evaluates the combined results.
10. Revision Loop – Allows up to two improvement attempts.
11. Streamlit Dashboard – Displays results, progress and execution history.

The complete implementation is saved in `app.py`.

## 8\. Run the Application

Ensure Ollama is running and Qwen3 is available.

Start Streamlit:

bash

```bash
streamlit run app.py
```

Open:

text

```text
http://localhost:8501
```

Enter a task and click **Start Multi-Agent Workflow**.

## 9\. Workflow Execution

When a user submits a request:

1. Coordinator sends the request to Qwen3.
2. Coordinator generates three structured tasks.
3. Pydantic validates the task assignments.
4. NetworkX validates task dependencies.
5. Independent specialist agents execute concurrently.
6. Results are collected and shared through workflow context.
7. Reviewer evaluates the results.
8. Incomplete results enter the revision process.
9. Final response is generated.
10. SQLite stores execution history and final results.
11. Streamlit displays agent outputs and execution information.

## 10\. Testing Scenarios

### Test 1: DevOps

text

```text
Design an AWS deployment architecture for a Python
application using Docker and CI/CD.

Include security, monitoring, load balancing
and rollback procedures.
```

Expected: Research, architecture analysis, implementation recommendations and reviewer feedback.

### Test 2: ERP

text

```text
Design an employee attendance reporting system.

Analyze absenteeism, late arrivals and attendance
trends, and prepare management reporting recommendations.
```

Expected: Attendance analysis and reporting workflow.

### Test 3: Software Development

text

```text
Design a task management application using Python,
FastAPI, PostgreSQL and React.

Include architecture, API design, database tables,
testing and deployment.
```

Expected: A coordinated software development plan.

## 11\. Database Verification

Open `agents.db` using DB Browser for SQLite.

Verify these tables:

- `executions` – Agent names, statuses, outputs and execution times.
- `runs` – User requests and final responses.

Confirm that workflow records remain available after restarting the application.

## 12\. Final Verification Checklist

- [ ]Python environment configured.
- [ ]Ollama installed and running.
- [ ]Qwen3 downloaded successfully.
- [ ]Dependencies installed.
- [ ]Coordinator generates structured tasks.
- [ ]Specialist agents execute independently.
- [ ]Parallel execution works.
- [ ]Shared context passes agent results.
- [ ]Reviewer evaluates responses.
- [ ]Revision mechanism works.
- [ ]SQLite stores workflow history.
- [ ]Streamlit dashboard displays results.
- [ ]DevOps, ERP and software development scenarios tested.

## 13\. Final Outcome

Successfully built a local AI multi-agent collaboration system using Python and Ollama.

**Key learning outcomes:**

- Multi-agent architecture.
- AI task delegation.
- Parallel execution.
- Agent communication and shared context.
- Structured AI responses.
- Quality evaluation and revision loops.
- Workflow monitoring.
- SQLite persistence.
- Streamlit dashboard development.

**Day 39 Key Takeaway:** Multiple specialized AI agents can collaborate through task delegation, shared results and independent review to solve complex problems more effectively than a single undirected chatbot.

**Project Status:** Complete after successful execution and verification of all acceptance checks.

# Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/a0a6e4f3-db65-41b0-88fc-a40f878ba70b" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/320f8930-25a2-4a24-8ac8-9462ab830cdc" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/800c137f-2467-4b58-9df8-6100ab7cfcb8" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/c5ca1184-15b8-40cf-ad52-a3d6c7ff0cc9" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/df893cd5-0f59-45ab-9fbb-933a03c7409e" />





