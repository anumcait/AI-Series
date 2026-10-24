import json
import sqlite3
import time
import uuid
from datetime import datetime, timezone

import httpx
import pandas as pd
import plotly.express as px
import streamlit as st

OLLAMA_URL = "http://localhost:11434"
DB_PATH = "monitor.db"
DEFAULT_MODEL = "qwen3:4b"


# -----------------------------
# 1. Database setup
# -----------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                request_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                model TEXT NOT NULL,
                latency_ms REAL,
                status TEXT NOT NULL,
                prompt_tokens INTEGER,
                output_tokens INTEGER,
                load_ms REAL,
                generation_ms REAL,
                tokens_per_second REAL,
                error_type TEXT
            )
        """)


def save_request(record):
    with get_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO requests (
                request_id, timestamp, model, latency_ms,
                status, prompt_tokens, output_tokens, load_ms,
                generation_ms, tokens_per_second, error_type
            ) VALUES (
                :request_id, :timestamp, :model, :latency_ms,
                :status, :prompt_tokens, :output_tokens, :load_ms,
                :generation_ms, :tokens_per_second, :error_type
            )
        """, record)


def load_requests():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT * FROM requests ORDER BY timestamp DESC
        """).fetchall()

    return pd.DataFrame([dict(row) for row in rows])


# -----------------------------
# 2. Ollama model discovery
# -----------------------------
def get_models():
    response = httpx.get(
        f"{OLLAMA_URL}/api/tags",
        timeout=3,
    )
    response.raise_for_status()

    return [
        model["name"]
        for model in response.json().get("models", [])
    ]


# -----------------------------
# 3. Request metrics
# -----------------------------
def new_record(request_id, model):
    return {
        "request_id": request_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "latency_ms": None,
        "status": "failed",
        "prompt_tokens": None,
        "output_tokens": None,
        "load_ms": None,
        "generation_ms": None,
        "tokens_per_second": None,
        "error_type": None,
    }


def stream_answer(prompt, model, record):
    started = time.perf_counter()
    record["status"] = "failed"
    first_error = None

    try:
        with httpx.stream(
            "POST",
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True,
            },
            timeout=httpx.Timeout(
                connect=5,
                read=180,
                write=10,
                pool=5,
            ),
        ) as response:

            response.raise_for_status()
            finished = False

            for line in response.iter_lines():
                if not line:
                    continue

                chunk = json.loads(line)

                text = chunk.get("message", {}).get("content", "")
                if text:
                    yield text

                if chunk.get("done"):
                    finished = True

                    # Ollama reports timing in nanoseconds.
                    prompt_count = chunk.get("prompt_eval_count")
                    output_count = chunk.get("eval_count")
                    load_duration = chunk.get("load_duration")
                    eval_duration = chunk.get("eval_duration")

                    record["prompt_tokens"] = prompt_count
                    record["output_tokens"] = output_count

                    if load_duration is not None:
                        record["load_ms"] = load_duration / 1_000_000

                    if eval_duration is not None:
                        record["generation_ms"] = (
                            eval_duration / 1_000_000
                        )

                    if (
                        output_count is not None
                        and eval_duration is not None
                        and eval_duration > 0
                    ):
                        record["tokens_per_second"] = (
                            output_count * 1_000_000_000
                            / eval_duration
                        )

                    break

            if finished:
                record["status"] = "success"
            else:
                record["error_type"] = "IncompleteStream"

    except httpx.TimeoutException:
        record["error_type"] = "TimeoutException"
        first_error = "Ollama request timed out."

    except httpx.HTTPStatusError as exc:
        record["error_type"] = f"HTTP_{exc.response.status_code}"
        first_error = (
            f"Ollama returned HTTP {exc.response.status_code}."
        )

    except httpx.HTTPError:
        record["error_type"] = "ConnectionError"
        first_error = "Could not connect to Ollama."

    except (ValueError, KeyError):
        record["error_type"] = "InvalidResponse"
        first_error = "Ollama returned an invalid response."

    except Exception:
        record["error_type"] = "UnexpectedError"
        first_error = "An unexpected inference error occurred."

    finally:
        record["latency_ms"] = (
            time.perf_counter() - started
        ) * 1000

        save_request(record)

    if first_error:
        st.error(first_error)
    elif record["status"] != "success":
        st.error("The response stream ended before completion.")


# -----------------------------
# 4. Dashboard
# -----------------------------
st.set_page_config(
    page_title="Local LLM Observability",
    page_icon="📊",
    layout="wide",
)

init_db()

st.title("📊 Local LLM Observability Dashboard")
st.caption("Ollama · Qwen3 · SQLite · Streamlit")

with st.sidebar:
    st.header("Settings")

    if st.button("Refresh dashboard"):
        st.rerun()

    try:
        models = get_models()
        model_error = None
    except httpx.HTTPError:
        models = []
        model_error = "Ollama is unreachable."

    if model_error:
        st.error(model_error)

    if models:
        default_index = (
            models.index(DEFAULT_MODEL)
            if DEFAULT_MODEL in models
            else 0
        )

        selected_model = st.selectbox(
            "Ollama model",
            models,
            index=default_index,
        )
    else:
        selected_model = None
        st.warning("Start Ollama and download a model.")

    st.caption("Prompt text and model responses are not stored in SQLite.")

st.subheader("Run an inference request")

prompt = st.text_area(
    "Your question",
    placeholder="Explain the difference between latency and throughput.",
    max_chars=4000,
)

if st.button("Run model", type="primary"):
    if not selected_model:
        st.error("No model is available. Check Ollama.")
    elif not prompt.strip():
        st.warning("Enter a question first.")
    else:
        request_id = str(uuid.uuid4())
        record = new_record(request_id, selected_model)

        st.write(f"Request ID: `{request_id}`")
        st.write("**Model response**")

        with st.spinner("Generating response..."):
            st.write_stream(
                stream_answer(prompt, selected_model, record)
            )

        st.caption(
            f"Status: {record['status']} · "
            f"Latency: {record['latency_ms']:.0f} ms"
        )

        st.rerun()


# -----------------------------
# 5. Load actual observations
# -----------------------------
df = load_requests()

st.divider()
st.subheader("Performance overview")

if df.empty:
    st.info(
        "No requests have been recorded yet. "
        "Submit a prompt above to populate the dashboard."
    )
else:
    total = len(df)
    successes = int((df["status"] == "success").sum())
    failures = total - successes
    success_rate = successes / total * 100

    successful_latency = df.loc[
        df["status"] == "success", "latency_ms"
    ].dropna()

    average_latency = (
        successful_latency.mean()
        if not successful_latency.empty
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total requests", total)
    c2.metric("Avg latency", f"{average_latency / 1000:.2f} s")
    c3.metric("Success rate", f"{success_rate:.1f}%")
    c4.metric("Errors", failures)

    left, right = st.columns(2)

    with left:
        st.markdown("**Latency over time**")

        chart_df = df.dropna(subset=["latency_ms"]).sort_values(
            "timestamp"
        )

        if not chart_df.empty:
            fig = px.line(
                chart_df,
                x="timestamp",
                y="latency_ms",
                color="model",
                markers=True,
                title="End-to-end latency (ms)",
            )
            st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("**Token usage per request**")

        token_df = df.dropna(
            subset=["prompt_tokens", "output_tokens"]
        )

        if not token_df.empty:
            token_long = token_df.melt(
                id_vars=["timestamp", "model"],
                value_vars=["prompt_tokens", "output_tokens"],
                var_name="token_type",
                value_name="tokens",
            )

            fig = px.bar(
                token_long,
                x="timestamp",
                y="tokens",
                color="token_type",
                barmode="group",
                title="Prompt vs generated tokens",
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Model comparison**")

    comparison = df.groupby("model").agg(
        requests=("request_id", "count"),
        success_rate=("status", lambda x: (
            x == "success"
        ).mean() * 100),
        avg_latency_ms=("latency_ms", "mean"),
        avg_output_tokens=("output_tokens", "mean"),
        avg_tokens_per_second=("tokens_per_second", "mean"),
    ).reset_index()

    st.dataframe(comparison, use_container_width=True)

    st.markdown("**Request history**")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Export request history to CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="llm_metrics.csv",
        mime="text/csv",
    )