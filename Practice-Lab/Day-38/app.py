
import streamlit as st
import ollama
import networkx as nx
import plotly.graph_objects as go
import sqlite3
import json
import uuid
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

DB = "workflow.db"
MODEL = "qwen3:4b"

# ---------- DATABASE ----------

def db():
    return sqlite3.connect(DB, check_same_thread=False)

def initialize():
    with db() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS runs(
            id TEXT PRIMARY KEY,
            ticket TEXT,
            status TEXT,
            created TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        con.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            run_id TEXT,
            name TEXT,
            status TEXT,
            output TEXT,
            error TEXT,
            attempts INTEGER DEFAULT 0,
            PRIMARY KEY(run_id, name)
        )
        """)

def update_task(run_id, name, status, output="", error="", attempts=0):
    with db() as con:
        con.execute("""
        UPDATE tasks SET status=?, output=?, error=?, attempts=?
        WHERE run_id=? AND name=?
        """, (status, output, error, attempts, run_id, name))

def ask_ai(prompt):
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# ---------- WORKFLOW DEFINITION ----------

TASKS = {
    "classify": {
        "deps": [],
        "prompt": lambda ticket, results:
            f"Classify this support ticket. Return category and priority "
            f"(High or Normal). Ticket: {ticket}"
    },
    "analyze": {
        "deps": ["classify"],
        "prompt": lambda ticket, results:
            f"Analyze this ticket. Extract issue, payment details and "
            f"recommended next action. Ticket: {ticket}"
    },
    "sentiment": {
        "deps": ["classify"],
        "prompt": lambda ticket, results:
            f"Analyze customer sentiment and urgency. Ticket: {ticket}"
    },
    "decision": {
        "deps": ["analyze", "sentiment"],
        "prompt": None
    },
    "urgent_response": {
        "deps": ["decision"],
        "prompt": lambda ticket, results:
            f"Write an empathetic URGENT support response. "
            f"Analysis: {results['analyze']} "
            f"Sentiment: {results['sentiment']}"
    },
    "standard_response": {
        "deps": ["decision"],
        "prompt": lambda ticket, results:
            f"Write a polite STANDARD support response. "
            f"Analysis: {results['analyze']} "
            f"Sentiment: {results['sentiment']}"
    }
}

GRAPH = nx.DiGraph()
for name, task in TASKS.items():
    GRAPH.add_node(name)
    for dep in task["deps"]:
        GRAPH.add_edge(dep, name)

# ---------- TASK EXECUTION ----------

def execute_task(run_id, name, ticket, results, branch):
    attempts = 0
    update_task(run_id, name, "Running")

    while attempts < 3:
        attempts += 1
        try:
            if name == "decision":
                priority = results["classify"].lower()
                branch["urgent"] = (
                    "high" in priority or "urgent" in priority
                )
                output = "Urgent branch selected" if branch["urgent"] \
                    else "Standard branch selected"
            else:
                prompt = TASKS[name]["prompt"](ticket, results)
                output = ask_ai(prompt)

            results[name] = output
            update_task(
                run_id, name, "Completed",
                output=output, attempts=attempts
            )
            return name

        except Exception as e:
            update_task(
                run_id, name, "Running",
                error=str(e), attempts=attempts
            )
            time.sleep(2)

    update_task(
        run_id, name, "Failed",
        error="Maximum retries reached", attempts=attempts
    )
    raise RuntimeError(f"{name} failed after 3 attempts")

def run_workflow(run_id, ticket):
    results = {}
    branch = {}
    completed = set()
    running = {}

    with ThreadPoolExecutor(max_workers=3) as pool:
        while len(completed) < len(TASKS):

            # Process finished tasks
            done = [f for f in running if f.done()]
            for future in done:
                name = running.pop(future)
                try:
                    future.result()
                    completed.add(name)
                except Exception:
                    # Stop dependent tasks after failure
                    with db() as con:
                        con.execute(
                            "UPDATE runs SET status='Failed' WHERE id=?",
                            (run_id,)
                        )
                    for task_name in TASKS:
                        if task_name not in completed:
                            update_task(
                                run_id, task_name, "Blocked",
                                error="Dependency failed"
                            )
                    return

            # Find tasks whose dependencies have completed
            for name, task in TASKS.items():
                if name in completed or name in running.values():
                    continue

                if not all(d in completed for d in task["deps"]):
                    continue

                # Conditional branch
                if name == "urgent_response" and not branch.get("urgent", False):
                    update_task(run_id, name, "Skipped")
                    completed.add(name)
                    continue

                if name == "standard_response" and branch.get("urgent", False):
                    update_task(run_id, name, "Skipped")
                    completed.add(name)
                    continue

                future = pool.submit(
                    execute_task, run_id, name, ticket, results, branch
                )
                running[future] = name

            if running:
                wait(running.keys(), return_when=FIRST_COMPLETED)
            elif len(completed) < len(TASKS):
                break

    status = "Completed" if len(completed) == len(TASKS) else "Failed"
    with db() as con:
        con.execute(
            "UPDATE runs SET status=? WHERE id=?",
            (status, run_id)
        )

# ---------- START WORKFLOW ----------

def start_workflow(ticket):
    run_id = str(uuid.uuid4())

    with db() as con:
        con.execute(
            "INSERT INTO runs(id,ticket,status) VALUES(?,?,?)",
            (run_id, ticket, "Running")
        )
        for name in TASKS:
            con.execute(
                "INSERT INTO tasks(run_id,name,status) VALUES(?,?,?)",
                (run_id, name, "Pending")
            )

    thread = threading.Thread(
        target=run_workflow,
        args=(run_id, ticket),
        daemon=True
    )
    thread.start()
    return run_id

# ---------- STREAMLIT DASHBOARD ----------

st.set_page_config(page_title="Day 38 AI Workflow", layout="wide")
initialize()

st.title("🚀 Day 38 - AI Workflow Orchestration Engine")
st.caption("Local AI automation powered by Ollama and Qwen3")

ticket = st.text_area(
    "Enter customer support ticket",
    "My payment was deducted, but my order is still unpaid. Please resolve this urgently."
)

if st.button("▶ Start Workflow", type="primary"):
    if ticket.strip():
        st.session_state.run_id = start_workflow(ticket)
    else:
        st.warning("Please enter a ticket.")

run_id = st.session_state.get("run_id")

if run_id:
    with db() as con:
        run = con.execute(
            "SELECT status FROM runs WHERE id=?", (run_id,)
        ).fetchone()

        tasks = con.execute(
            "SELECT name,status,output,error,attempts FROM tasks WHERE run_id=?",
            (run_id,)
        ).fetchall()

    st.subheader("Workflow Execution Monitor")
    st.write("Workflow status:", run[0])

    for name, status, output, error, attempts in tasks:
        st.write(f"**{name}** — {status} | Attempts: {attempts}")
        if output:
            st.caption(output)
        if error:
            st.error(error)

    # Pipeline visualization
    colors = {
        "Pending": "gray",
        "Running": "orange",
        "Completed": "green",
        "Failed": "red",
        "Skipped": "lightblue",
        "Blocked": "darkred"
    }

    task_status = {t[0]: t[1] for t in tasks}
    positions = {
        "classify": (0, 3),
        "analyze": (-1, 2),
        "sentiment": (1, 2),
        "decision": (0, 1),
        "urgent_response": (-1, 0),
        "standard_response": (1, 0)
    }

    fig = go.Figure()
    for a, b in GRAPH.edges():
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        fig.add_trace(go.Scatter(
            x=[x1, x2], y=[y1, y2],
            mode="lines",
            line=dict(color="gray", width=2),
            showlegend=False
        ))

    for name, (x, y) in positions.items():
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            text=[f"{name}<br>{task_status.get(name, 'Pending')}"],
            textposition="bottom center",
            marker=dict(
                size=35,
                color=colors.get(task_status.get(name), "gray")
            ),
            showlegend=False
        ))

    fig.update_layout(
        title="Live Workflow Pipeline",
        height=500,
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Refresh while processing
    if run[0] == "Running":
        time.sleep(2)
        st.rerun()

# ---------- HISTORY ----------

st.divider()
st.subheader("📚 Workflow History")

with db() as con:
    history = con.execute(
        "SELECT id,ticket,status,created FROM runs ORDER BY created DESC"
    ).fetchall()

for rid, text, status, created in history:
    with st.expander(f"{created} | {status} | {rid[:8]}"):
        st.write("Ticket:", text)
        with db() as con:
            saved = con.execute(
                "SELECT name,status,output,error,attempts FROM tasks WHERE run_id=?",
                (rid,)
            ).fetchall()
        for task in saved:
            st.write(task[0], "-", task[1], "| Attempts:", task[4])
            if task[2]:
                st.write(task[2])
            if task[3]:
                st.error(task[3])
