import json
import sqlite3
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

import networkx as nx
import ollama
import pandas as pd
import plotly.express as px
import streamlit as st
from pydantic import BaseModel, Field

# ---------------- CONFIGURATION ----------------

MODEL = "qwen3:4b"
DB = "agents.db"
MAX_REVISIONS = 2

AGENTS = {
    "research": "You are a research specialist. Identify relevant facts, assumptions and information gaps.",
    "analysis": "You are an analysis specialist. Examine the problem, identify causes, risks and conclusions.",
    "execution": "You are an implementation specialist. Provide practical, safe, ordered implementation steps. Never claim you executed actions."
}

# ---------------- STRUCTURED OUTPUTS ----------------

class Task(BaseModel):
    agent: str
    instruction: str
    depends_on: list[str] = Field(default_factory=list)

class Plan(BaseModel):
    tasks: list[Task]

class Review(BaseModel):
    approved: bool
    score: int
    feedback: str

# ---------------- DATABASE ----------------

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT,
            agent TEXT,
            status TEXT,
            output TEXT,
            seconds REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            request TEXT,
            final_answer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

def save_execution(run_id, agent, status, output="", seconds=0):
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        INSERT INTO executions
        (run_id, agent, status, output, seconds)
        VALUES (?, ?, ?, ?, ?)
        """, (run_id, agent, status, output, seconds))

# ---------------- AI HELPER ----------------

def ask_ai(system, prompt, schema=None):
    kwargs = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "options": {"temperature": 0.2}
    }

    if schema:
        kwargs["format"] = schema.model_json_schema()

    response = ollama.chat(**kwargs)
    return response.message.content

# ---------------- COORDINATOR ----------------

def create_plan(request):
    system = """
    You are the Coordinator Agent.
    Divide the user's request into exactly three independent tasks:
    research, analysis and execution.
    Use only these three agent names.
    Return structured JSON matching the supplied schema.
    Every task must have a clear instruction.
    Use depends_on to identify task dependencies.
    """

    result = ask_ai(system, request, Plan)
    plan = Plan.model_validate_json(result)

    if len(plan.tasks) != 3:
        raise ValueError("Coordinator must create exactly three tasks.")

    if {task.agent for task in plan.tasks} != set(AGENTS):
        raise ValueError("Invalid agent assignments.")

    graph = nx.DiGraph()

    for task in plan.tasks:
        graph.add_node(task.agent)

    for task in plan.tasks:
        for dependency in task.depends_on:
            if dependency not in AGENTS:
                raise ValueError("Unknown task dependency.")
            graph.add_edge(dependency, task.agent)

    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("Task dependencies contain a cycle.")

    return plan, graph

# ---------------- SPECIALIST AGENTS ----------------

def run_agent(task, shared_context, feedback=""):
    start = time.perf_counter()

    prompt = f"""
    Your assigned task:
    {task.instruction}

    Original user request and shared agent context:
    {shared_context}

    Reviewer feedback, if any:
    {feedback}

    Complete only your assigned responsibility.
    Clearly identify assumptions and limitations.
    """

    output = ask_ai(AGENTS[task.agent], prompt)
    elapsed = round(time.perf_counter() - start, 2)

    return {
        "agent": task.agent,
        "output": output,
        "seconds": elapsed,
        "status": "completed"
    }

# ---------------- REVIEWER ----------------

def review_results(request, results):
    context = json.dumps(results, indent=2)

    system = """
    You are an independent quality Reviewer Agent.
    Evaluate factual consistency, completeness, relevance,
    practical usefulness and contradictions.
    Approve only if the response is sufficiently complete.
    Return JSON matching the supplied schema.
    """

    result = ask_ai(
        system,
        f"User request:\n{request}\nAgent results:\n{context}",
        Review
    )

    return Review.model_validate_json(result)

# ---------------- ORCHESTRATION ----------------

def run_workflow(request, update):
    run_id = str(uuid.uuid4())
    save_execution(run_id, "coordinator", "running")

    plan, graph = create_plan(request)

    save_execution(
        run_id, "coordinator", "completed",
        plan.model_dump_json()
    )

    update("Coordinator created the task plan.")

    results = {}
    remaining = {task.agent: task for task in plan.tasks}

    # Execute tasks only after dependencies finish.
    while remaining:
        ready = [
            task for task in remaining.values()
            if all(dep in results for dep in task.depends_on)
        ]

        if not ready:
            raise ValueError("Unable to resolve task dependencies.")

        for task in ready:
            save_execution(run_id, task.agent, "running")

        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = {
                pool.submit(
                    run_agent,
                    task,
                    json.dumps({
                        "request": request,
                        "previous_results": results
                    })
                ): task
                for task in ready
            }

            for future in as_completed(futures):
                task = futures[future]

                try:
                    result = future.result()
                    results[task.agent] = result

                    save_execution(
                        run_id, task.agent, "completed",
                        result["output"], result["seconds"]
                    )

                    update(f"{task.agent} agent completed.")

                except Exception as error:
                    save_execution(
                        run_id, task.agent, "failed", str(error)
                    )
                    raise

                del remaining[task.agent]

    # Reviewer and revision cycle
    approved = False
    final_review = None
    revision_feedback = ""

    for attempt in range(MAX_REVISIONS + 1):
        update(f"Reviewer checking results (attempt {attempt + 1}).")

        final_review = review_results(request, results)

        save_execution(
            run_id, "reviewer",
            "approved" if final_review.approved else "revision",
            final_review.model_dump_json()
        )

        if final_review.approved:
            approved = True
            break

        revision_feedback = final_review.feedback

        if attempt < MAX_REVISIONS:
            update("Reviewer requested improvements.")

            revision = ask_ai(
                "You are a revision specialist. Improve the combined "
                "answer using reviewer feedback. Do not invent facts.",
                f"""
                Original request: {request}
                Previous results: {json.dumps(results)}
                Reviewer feedback: {revision_feedback}
                Produce the improved final answer.
                """
            )

            results["revision"] = {
                "agent": "revision",
                "output": revision,
                "status": "completed"
            }

    if not approved:
        final_answer = (
            "Review was not approved after the revision limit.\n\n"
            + revision_feedback
            + "\n\nDraft results:\n"
            + json.dumps(results, indent=2)
        )
    else:
        final_answer = results.get(
            "revision",
            {"output": "\n\n".join(
                item["output"] for item in results.values()
            )}
        )["output"]

    with sqlite3.connect(DB) as conn:
        conn.execute("""
        INSERT INTO runs (run_id, request, final_answer)
        VALUES (?, ?, ?)
        """, (run_id, request, final_answer))

    update("Workflow finished. Results saved to SQLite.")

    return run_id, final_answer, results, final_review, graph

# ---------------- STREAMLIT DASHBOARD ----------------

st.set_page_config(
    page_title="Day 39 Multi-Agent System",
    page_icon="🚀",
    layout="wide"
)

init_db()

st.title("🚀 Local AI Multi-Agent Collaboration System")
st.caption(f"Powered by Ollama + {MODEL}")

st.sidebar.success("Local AI system")
st.sidebar.write("Coordinator → Specialists → Reviewer → SQLite")

request = st.text_area(
    "Enter your task",
    placeholder="Example: Design a secure AWS deployment plan for a Python application.",
    height=120
)

if st.button("🚀 Start Multi-Agent Workflow", type="primary"):
    if not request.strip():
        st.warning("Please enter a task.")
    else:
        progress = st.empty()
        status = st.status("Starting agents...", expanded=True)

        def update(message):
            progress.write("🔄 " + message)
            status.write(message)

        try:
            run_id, answer, results, review, graph = run_workflow(
                request, update
            )

            status.update(
                label="Workflow completed",
                state="complete"
            )

            st.session_state["answer"] = answer
            st.session_state["results"] = results
            st.session_state["run_id"] = run_id
            st.session_state["review"] = review

        except Exception as error:
            status.update(label="Workflow failed", state="error")
            st.error(str(error))

if "answer" in st.session_state:
    st.divider()
    st.subheader("🏆 Final Result")
    st.markdown(st.session_state["answer"])

    st.subheader("🤖 Individual Agent Results")

    for name, result in st.session_state["results"].items():
        with st.expander(name.upper()):
            st.write(result["output"])

    review = st.session_state["review"]

    st.subheader("Reviewer Evaluation")
    st.write("Approved:", review.approved)
    st.write("Quality score:", review.score, "/ 100")
    st.write(review.feedback)

    st.caption("Run ID: " + st.session_state["run_id"])

# ---------------- EXECUTION HISTORY ----------------

st.divider()
st.header("📊 Execution Dashboard")

with sqlite3.connect(DB) as conn:
    history = pd.read_sql_query(
        "SELECT * FROM executions ORDER BY id DESC LIMIT 100",
        conn
    )
    runs = pd.read_sql_query(
        "SELECT * FROM runs ORDER BY created_at DESC",
        conn
    )

if not history.empty:
    col1, col2, col3 = st.columns(3)

    col1.metric("Agent executions", len(history))
    col2.metric(
        "Completed",
        int((history["status"] == "completed").sum())
    )
    col3.metric(
        "Failed",
        int((history["status"] == "failed").sum())
    )

    st.subheader("Agent Execution Records")
    st.dataframe(history, use_container_width=True)

    completed = history[
        (history["status"] == "completed")
        & (history["seconds"] > 0)
    ]

    if not completed.empty:
        fig = px.bar(
            completed,
            x="agent",
            y="seconds",
            color="agent",
            title="Agent Execution Time (seconds)"
        )
        st.plotly_chart(fig, use_container_width=True)

if not runs.empty:
    st.subheader("Previous Workflow History")
    st.dataframe(
        runs[["run_id", "request", "created_at"]],
        use_container_width=True
    )
