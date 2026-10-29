import sqlite3
import threading
import time
import uuid
from datetime import datetime, timezone

import requests
import streamlit as st

DB = "jobs.db"
MODEL = "qwen3:4b"
OLLAMA_URL = "http://localhost:11434/api/generate"
MAX_ATTEMPTS = 3

# ---------- Time and database ----------

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect():
    con = sqlite3.connect(DB, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA busy_timeout=30000")
    return con


def init_db():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                task TEXT NOT NULL,
                prompt TEXT NOT NULL,
                priority INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'Pending',
                attempts INTEGER NOT NULL DEFAULT 0,
                result TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                started_at TEXT,
                finished_at TEXT
            )
        """)
        con.execute("""
            CREATE INDEX IF NOT EXISTS idx_jobs_queue
            ON jobs(status, priority DESC, created_at ASC)
        """)
        # Recover work interrupted by an app restart.
        con.execute("""
            UPDATE jobs SET status='Pending',
                started_at=NULL,
                error='Recovered after application restart'
            WHERE status='Running'
        """)


def submit_job(task, prompt, priority):
    job_id = str(uuid.uuid4())
    with connect() as con:
        con.execute("""
            INSERT INTO jobs
            (id, task, prompt, priority, status, created_at)
            VALUES (?, ?, ?, ?, 'Pending', ?)
        """, (job_id, task, prompt, priority, now()))
    return job_id


def claim_job():
    # Claim and update in one transaction.
    with connect() as con:
        con.execute("BEGIN IMMEDIATE")
        job = con.execute("""
            SELECT * FROM jobs
            WHERE status='Pending' AND attempts < ?
            ORDER BY priority DESC, created_at ASC
            LIMIT 1
        """, (MAX_ATTEMPTS,)).fetchone()

        if job is None:
            return None

        con.execute("""
            UPDATE jobs SET status='Running',
                attempts=attempts+1, started_at=?,
                finished_at=NULL, error=NULL
            WHERE id=? AND status='Pending'
        """, (now(), job["id"]))

        return dict(job)


# ---------- AI task execution ----------

def make_prompt(task, text):
    instructions = {
        "Summarization": "Summarize the following text clearly and concisely.",
        "Translation": "Translate the following text into English.",
        "Question answering": "Answer the question using the supplied text. If needed, state when the text lacks the answer."
    }
    return f"{instructions[task]}\n\nInput:\n{text}"


def run_ai(task, text):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": make_prompt(task, text),
            "stream": False
        },
        timeout=(5, 300)
    )
    response.raise_for_status()
    result = response.json().get("response", "").strip()
    if not result:
        raise RuntimeError("Ollama returned an empty response")
    return result


def worker_loop():
    while True:
        job = claim_job()

        if job is None:
            time.sleep(1)
            continue

        try:
            result = run_ai(job["task"], job["prompt"])
            with connect() as con:
                con.execute("""
                    UPDATE jobs SET status='Completed',
                        result=?, error=NULL, finished_at=?
                    WHERE id=? AND status='Running'
                """, (result, now(), job["id"]))

        except Exception as exc:
            with connect() as con:
                current = con.execute(
                    "SELECT attempts FROM jobs WHERE id=?",
                    (job["id"],)
                ).fetchone()
                attempts = current["attempts"]
                status = (
                    "Pending" if attempts < MAX_ATTEMPTS
                    else "Failed"
                )
                con.execute("""
                    UPDATE jobs SET status=?, error=?,
                        finished_at=?
                    WHERE id=? AND status='Running'
                """, (
                    status, str(exc)[:1000], now(), job["id"]
                ))
            if status == "Pending":
                time.sleep(2)


# ---------- Start worker once per app process ----------

init_db()

if not hasattr(st, "_day37_worker_started"):
    st._day37_worker_started = True
    threading.Thread(
        target=worker_loop,
        name="day37-worker",
        daemon=True
    ).start()


# ---------- Streamlit dashboard ----------

st.set_page_config(page_title="Day 37 AI Job Queue", layout="wide")
st.title("⚙️ Local AI Task Queue")
st.caption(f"Model: {MODEL} | SQLite persistent queue | Background worker")

with st.form("submit_job"):
    task = st.selectbox(
        "Task type",
        ["Summarization", "Translation", "Question answering"]
    )
    prompt = st.text_area(
        "Text or question",
        placeholder="Enter the text to process...",
        height=150
    )
    priority = st.selectbox(
        "Priority", ["Normal", "High"]
    )
    submitted = st.form_submit_button("Queue AI task")

if submitted:
    if not prompt.strip():
        st.error("Please enter text before submitting.")
    else:
        job_id = submit_job(
            task, prompt.strip(),
            10 if priority == "High" else 0
        )
        st.session_state["last_job_id"] = job_id
        st.success(f"Job queued: {job_id}")

if st.session_state.get("last_job_id"):
    st.code(st.session_state["last_job_id"])

@st.fragment(run_every="3s")
def dashboard():
    with connect() as con:
        rows = con.execute("""
            SELECT * FROM jobs
            ORDER BY created_at DESC
        """).fetchall()

    jobs = [dict(row) for row in rows]
    pending = sum(j["status"] == "Pending" for j in jobs)
    running = sum(j["status"] == "Running" for j in jobs)
    completed = [j for j in jobs if j["status"] == "Completed"]
    failed = sum(j["status"] == "Failed" for j in jobs)

    a, b, c, d = st.columns(4)
    a.metric("Pending", pending)
    b.metric("Running", running)
    c.metric("Completed", len(completed))
    d.metric("Failed", failed)

    terminal = len(completed) + failed
    st.metric(
        "Success rate",
        f"{100 * len(completed) / terminal:.1f}%"
        if terminal else "—"
    )

    st.subheader("Job history")
    for j in jobs:
        with st.expander(
            f'{j["status"]} | {j["task"]} | {j["id"][:8]}'
        ):
            st.write("**Job ID:**", j["id"])
            st.write("**Priority:**", "High" if j["priority"] else "Normal")
            st.write("**Attempts:**", j["attempts"], "/", MAX_ATTEMPTS)
            st.write("**Submitted:**", j["created_at"])
            st.write("**Started:**", j["started_at"] or "Not started")
            st.write("**Finished:**", j["finished_at"] or "Not finished")
            if j["started_at"] and j["finished_at"]:
                start = datetime.fromisoformat(j["started_at"])
                end = datetime.fromisoformat(j["finished_at"])
                st.write("**Last attempt duration:**",
                         f"{(end - start).total_seconds():.1f} seconds")
            st.write("**Input:**", j["prompt"])
            if j["result"]:
                st.success("AI result")
                st.write(j["result"])
            if j["error"]:
                st.error(j["error"])

    if not jobs:
        st.info("No jobs yet. Submit your first task above.")

dashboard()