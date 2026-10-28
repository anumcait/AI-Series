import sqlite3
import time
from collections import defaultdict, deque
from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# ---------------- Configuration ----------------
DB_PATH = "requests.db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:4b"

RATE_LIMIT = 5          # requests per user
RATE_WINDOW = 60         # seconds
FAILURE_THRESHOLD = 3
RECOVERY_TIMEOUT = 30    # seconds before HALF_OPEN
REQUEST_TIMEOUT = (5, 120)  # connect timeout, response timeout
MAX_RETRIES = 1          # one retry after the first attempt

FALLBACK = (
    "The local AI service is temporarily unavailable. "
    "Please try again after the service recovers."
)

# ---------------- Persistent event history ----------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                username TEXT NOT NULL,
                status TEXT NOT NULL,
                latency_ms REAL,
                circuit_state TEXT NOT NULL,
                detail TEXT
            )
        """)

def log_event(username, status, latency_ms, circuit_state, detail=""):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO events
               (timestamp, username, status, latency_ms,
                circuit_state, detail)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                datetime.now(timezone.utc).isoformat(),
                username, status, latency_ms, circuit_state, detail
            ),
        )

def load_events():
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT * FROM events ORDER BY id DESC", conn
        )

init_db()

# ---------------- Shared in-process protection ----------------
# These controls are shared by browser sessions in this Python process.
# They reset when the Streamlit server process restarts.
if "rate_windows" not in st.session_state:
    st.session_state.rate_windows = {}

if "breaker" not in st.session_state:
    # The authoritative breaker is stored in module-level state below.
    pass

# Module-level state is shared by sessions in this server process.
# A production multi-worker deployment needs shared storage/atomic locks.
if "GLOBAL_STATE" not in globals():
    GLOBAL_STATE = {
        "rate_windows": defaultdict(deque),
        "breaker": {
            "state": "CLOSED",
            "failures": 0,
            "opened_at": 0.0,
            "probe_in_progress": False,
        },
    }

def get_breaker_state():
    breaker = GLOBAL_STATE["breaker"]

    if breaker["state"] == "OPEN":
        if time.monotonic() - breaker["opened_at"] >= RECOVERY_TIMEOUT:
            breaker["state"] = "HALF_OPEN"
            breaker["probe_in_progress"] = False

    return breaker["state"]

def allow_rate(username):
    now = time.monotonic()
    window = GLOBAL_STATE["rate_windows"][username]

    while window and now - window[0] >= RATE_WINDOW:
        window.popleft()

    if len(window) >= RATE_LIMIT:
        return False, int(RATE_WINDOW - (now - window[0]))

    window.append(now)
    return True, 0

def reserve_circuit():
    breaker = GLOBAL_STATE["breaker"]
    state = get_breaker_state()

    if state == "OPEN":
        return False, "Circuit is OPEN; calls are temporarily blocked."

    if state == "HALF_OPEN":
        if breaker["probe_in_progress"]:
            return False, "Recovery test already in progress; please retry shortly."
        breaker["probe_in_progress"] = True

    return True, ""

def record_success():
    breaker = GLOBAL_STATE["breaker"]
    breaker["state"] = "CLOSED"
    breaker["failures"] = 0
    breaker["probe_in_progress"] = False

def record_failure():
    breaker = GLOBAL_STATE["breaker"]
    breaker["probe_in_progress"] = False
    breaker["failures"] += 1

    if (
        breaker["state"] == "HALF_OPEN"
        or breaker["failures"] >= FAILURE_THRESHOLD
    ):
        breaker["state"] = "OPEN"
        breaker["opened_at"] = time.monotonic()

# ---------------- Ollama request with controlled retry ----------------
def ask_ollama(prompt):
    last_error = "Unknown Ollama error"

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "options": {
                    "num_predict": 256,
                },
            },
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()

            answer = data.get("response")
            if not answer:
                raise RuntimeError("Ollama returned no answer.")

            return answer, ""

        except (
            requests.RequestException,
            ValueError,
            RuntimeError,
        ) as exc:
            last_error = str(exc)
            if attempt < MAX_RETRIES:
                time.sleep(0.5)

    return None, last_error

# ---------------- Streamlit interface ----------------
# Shared across Streamlit reruns within this server process.
@st.cache_resource
def get_global_state():
    return {
        "rate_windows": defaultdict(deque),
        "breaker": {
            "state": "CLOSED",
            "failures": 0,
            "opened_at": 0.0,
            "probe_in_progress": False,
        },
    }

GLOBAL_STATE = get_global_state()

st.title("🛡️ Local AI Rate Limiter & Circuit Breaker")
st.caption("Day 36 | Python + Ollama + Qwen3 + SQLite")

with st.sidebar:
    st.header("Configuration")
    st.write(f"**Model:** `{MODEL}`")
    st.write(f"**Rate limit:** {RATE_LIMIT} requests / 60 seconds")
    st.write(f"**Failure threshold:** {FAILURE_THRESHOLD}")
    st.write(f"**Recovery wait:** {RECOVERY_TIMEOUT} seconds")
    st.write(f"**Timeout:** {REQUEST_TIMEOUT[1]} seconds per attempt")
    st.info("Use a consistent username to test the per-user limit.")

username = st.text_input("Test user ID", value="user1").strip()
prompt = st.text_area(
    "Your AI prompt",
    placeholder="Ask Qwen3 something...",
    height=110,
)

if st.button("Send AI Request", type="primary"):
    if not username:
        st.warning("Enter a user ID first.")
    elif not prompt.strip():
        st.warning("Enter a prompt first.")
    else:
        started = time.perf_counter()
        allowed, wait_seconds = allow_rate(username)

        if not allowed:
            state = get_breaker_state()
            log_event(
                username, "RATE_LIMITED", 0, state,
                f"Try again in about {wait_seconds} seconds."
            )
            st.error(
                f"Rate limit exceeded. Try again in about "
                f"{wait_seconds} seconds."
            )

        else:
            allowed_by_circuit, reason = reserve_circuit()

            if not allowed_by_circuit:
                state = get_breaker_state()
                log_event(username, "CIRCUIT_BLOCKED", 0, state, reason)
                st.error(reason)
                st.info(FALLBACK)

            else:
                with st.spinner("Checking Ollama and generating an answer..."):
                    answer, error = ask_ollama(prompt.strip())

                elapsed_ms = (time.perf_counter() - started) * 1000

                if answer is not None:
                    record_success()
                    state = get_breaker_state()
                    log_event(
                        username, "SUCCESS", elapsed_ms, state,
                        "AI response returned"
                    )
                    st.success("AI response")
                    st.markdown(answer)
                else:
                    record_failure()
                    state = get_breaker_state()
                    log_event(
                        username, "ERROR", elapsed_ms, state,
                        error[:500]
                    )
                    st.error(FALLBACK)
                    st.caption(f"Diagnostic detail: {error[:300]}")

                st.caption(f"Request duration: {elapsed_ms:.0f} ms")

st.divider()
st.subheader("Live operational dashboard")

# Refresh the page to update metrics after background/server activity.
if st.button("Refresh dashboard"):
    st.rerun()

breaker_state = get_breaker_state()
events = load_events()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total events", len(events))
col2.metric(
    "Successful calls",
    int((events["status"] == "SUCCESS").sum()) if not events.empty else 0,
)
col3.metric(
    "Rate-limited requests",
    int((events["status"] == "RATE_LIMITED").sum())
    if not events.empty else 0,
)
col4.metric("Circuit state", breaker_state)

if not events.empty:
    failures = int(
        events["status"].isin(["ERROR", "CIRCUIT_BLOCKED"]).sum()
    )
    st.metric("Errors + circuit blocks", failures)

    chart_data = (
        events.groupby("status").size()
        .reset_index(name="count")
    )
    st.plotly_chart(
    px.bar(
        chart_data,
        x="status",
        y="count",
        title="Request outcomes",
        text="count",
    ),
    width="stretch",
    config={"displayModeBar": True},
)

    st.subheader("Recent request history")
    st.dataframe(
        events.head(100),
        width="stretch",
        hide_index=True,
    )
else:
    st.info("No request events recorded yet. Send a prompt to begin.")

st.caption(
    "Circuit and rate-limit state are in memory; event history is stored "
    "in requests.db. Restarting the app resets protection state, not history."
)