# 🚀 Day 33 — Build a Local LLM Observability & Monitoring Dashboard 📊🤖

**Track:** 100 Days of AI | AI Engineering → LLMOps → MLOps

## Objective

Build a local LLM monitoring dashboard using Python, Ollama, Qwen3, Streamlit, SQLite, Pandas, and Plotly.

The application records request metrics, monitors performance, tracks failures, visualizes trends, and exports monitoring data to CSV.

## 1. Install Ollama and Qwen3

Install Ollama from https://ollama.com/download.

Verify the installation:

    ollama --version

Download the model:

    ollama pull qwen3:4b

Test inference:

    ollama run qwen3:4b

Enter a question and verify that the model responds. Type `/bye` to exit.

## 2. Create the Project

Create and activate a virtual environment:

    mkdir day33-llm-monitor
    cd day33-llm-monitor
    python -m venv .venv

Windows PowerShell:

    .venv\Scripts\Activate.ps1

macOS/Linux:

    source .venv/bin/activate

Install dependencies:

    python -m pip install streamlit httpx pandas plotly

Create the following files:

    day33-llm-monitor/
    ├── app.py
    └── .gitignore

Add the following to `.gitignore`:

    .venv/
    __pycache__/
    monitor.db
    *.pyc

## 3. Build the Monitoring Application

Create `app.py` with the following implementation:

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

    st.set_page_config(
        page_title="Local LLM Observability",
        page_icon="📊",
        layout="wide",
    )

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
                INSERT OR REPLACE INTO requests VALUES (
                    :request_id, :timestamp, :model, :latency_ms,
                    :status, :prompt_tokens, :output_tokens, :load_ms,
                    :generation_ms, :tokens_per_second, :error_type
                )
            """, record)

    def load_requests():
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM requests ORDER BY timestamp DESC"
            ).fetchall()
        return pd.DataFrame([dict(row) for row in rows])

    def get_models():
        response = httpx.get(
            f"{OLLAMA_URL}/api/tags", timeout=3
        )
        response.raise_for_status()
        return [
            item["name"]
            for item in response.json().get("models", [])
        ]

    def stream_answer(prompt, model, record):
        started = time.perf_counter()

        try:
            with httpx.stream(
                "POST",
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "stream": True,
                },
                timeout=httpx.Timeout(
                    connect=5, read=180, write=10, pool=5
                ),
            ) as response:

                response.raise_for_status()
                finished = False

                for line in response.iter_lines():
                    if not line:
                        continue

                    chunk = json.loads(line)
                    content = chunk.get(
                        "message", {}
                    ).get("content", "")

                    if content:
                        yield content

                    if chunk.get("done"):
                        finished = True

                        prompt_count = chunk.get(
                            "prompt_eval_count"
                        )
                        output_count = chunk.get("eval_count")
                        load_duration = chunk.get(
                            "load_duration"
                        )
                        eval_duration = chunk.get(
                            "eval_duration"
                        )

                        record["prompt_tokens"] = prompt_count
                        record["output_tokens"] = output_count

                        if load_duration is not None:
                            record["load_ms"] = (
                                load_duration / 1_000_000
                            )

                        if eval_duration is not None:
                            record["generation_ms"] = (
                                eval_duration / 1_000_000
                            )

                        if (
                            output_count is not None
                            and eval_duration
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
            st.error("Ollama request timed out.")

        except httpx.HTTPStatusError as exc:
            record["error_type"] = (
                f"HTTP_{exc.response.status_code}"
            )
            st.error(
                f"Ollama returned HTTP "
                f"{exc.response.status_code}."
            )

        except httpx.HTTPError:
            record["error_type"] = "ConnectionError"
            st.error("Could not connect to Ollama.")

        except (ValueError, KeyError):
            record["error_type"] = "InvalidResponse"
            st.error("Invalid response received from Ollama.")

        except Exception:
            record["error_type"] = "UnexpectedError"
            st.error("An unexpected inference error occurred.")

        finally:
            record["latency_ms"] = (
                time.perf_counter() - started
            ) * 1000
            save_request(record)

        if record["status"] != "success" and not record["error_type"]:
            record["error_type"] = "IncompleteStream"

    init_db()

    st.title("Local LLM Observability Dashboard")
    st.caption("Ollama | Qwen3 | SQLite | Streamlit")

    with st.sidebar:
        st.header("Settings")

        if st.button("Refresh dashboard"):
            st.rerun()

        try:
            models = get_models()
        except httpx.HTTPError:
            models = []
            st.error("Ollama is unreachable.")

        if models:
            index = (
                models.index(DEFAULT_MODEL)
                if DEFAULT_MODEL in models
                else 0
            )
            selected_model = st.selectbox(
                "Model", models, index=index
            )
        else:
            selected_model = None
            st.warning("Start Ollama and download a model.")

        st.caption(
            "Prompt text and responses are not saved in SQLite."
        )

    st.subheader("Run an inference request")

    prompt = st.text_area(
        "Your question",
        max_chars=4000,
        placeholder="Explain LLM observability.",
    )

    if st.button("Run model", type="primary"):
        if not selected_model:
            st.error("No model is available.")
        elif not prompt.strip():
            st.warning("Enter a question.")
        else:
            request_id = str(uuid.uuid4())

            record = {
                "request_id": request_id,
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "model": selected_model,
                "latency_ms": None,
                "status": "failed",
                "prompt_tokens": None,
                "output_tokens": None,
                "load_ms": None,
                "generation_ms": None,
                "tokens_per_second": None,
                "error_type": None,
            }

            st.write(f"Request ID: `{request_id}`")
            st.write("Model response")

            with st.spinner("Generating response..."):
                st.write_stream(
                    stream_answer(prompt, selected_model, record)
                )

            st.caption(
                f"Status: {record['status']} | "
                f"Latency: {record['latency_ms']:.0f} ms"
            )
            st.rerun()

    df = load_requests()

    st.divider()
    st.subheader("Performance overview")

    if df.empty:
        st.info("Submit a prompt to collect your first metrics.")
    else:
        total = len(df)
        successes = int((df["status"] == "success").sum())
        failures = total - successes
        success_rate = successes / total * 100

        latencies = df.loc[
            df["status"] == "success", "latency_ms"
        ].dropna()

        avg_latency = (
            latencies.mean() if not latencies.empty else 0
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total requests", total)
        c2.metric("Average latency", f"{avg_latency / 1000:.2f} s")
        c3.metric("Success rate", f"{success_rate:.1f}%")
        c4.metric("Errors", failures)

        left, right = st.columns(2)

        with left:
            chart_df = df.dropna(
                subset=["latency_ms"]
            ).sort_values("timestamp")

            if not chart_df.empty:
                fig = px.line(
                    chart_df,
                    x="timestamp",
                    y="latency_ms",
                    color="model",
                    markers=True,
                    title="Latency over time (ms)",
                )
                st.plotly_chart(
                    fig, use_container_width=True
                )

        with right:
            token_df = df.dropna(
                subset=["prompt_tokens", "output_tokens"]
            )

            if not token_df.empty:
                token_long = token_df.melt(
                    id_vars=["timestamp", "model"],
                    value_vars=[
                        "prompt_tokens", "output_tokens"
                    ],
                    var_name="token_type",
                    value_name="tokens",
                )

                fig = px.bar(
                    token_long,
                    x="timestamp",
                    y="tokens",
                    color="token_type",
                    barmode="group",
                    title="Token usage",
                )
                st.plotly_chart(
                    fig, use_container_width=True
                )

        st.subheader("Model comparison")

        comparison = df.groupby("model").agg(
            requests=("request_id", "count"),
            success_rate=(
                "status",
                lambda x: (x == "success").mean() * 100,
            ),
            avg_latency_ms=("latency_ms", "mean"),
            avg_output_tokens=("output_tokens", "mean"),
            avg_tokens_per_second=(
                "tokens_per_second", "mean"
            ),
        ).reset_index()

        st.dataframe(
            comparison, use_container_width=True
        )

        st.subheader("Request history")

        st.dataframe(
            df, use_container_width=True, hide_index=True
        )

        st.download_button(
            "Export request history to CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="llm_metrics.csv",
            mime="text/csv",
        )

## 4. Run the Dashboard

Ensure Ollama is running and verify its model list:

    ollama list

Start Streamlit:

    python -m streamlit run app.py

Open the local URL displayed in your terminal, usually:

    http://localhost:8501

Select `qwen3:4b`, enter a question, and click **Run model**.

## 5. Verify the Results

1. Submit three different prompts and confirm that request history grows.
2. Verify that latency, status, and available token metrics are recorded.
3. Stop Ollama and submit another request to test failure handling.
4. Restart Ollama and confirm that requests succeed again.
5. Download another model if your hardware permits, then compare its results.
6. Export the request history to CSV and inspect the downloaded file.

Ollama must be reachable at `http://localhost:11434`. The dashboard records request metadata in `monitor.db`, which is created automatically.

## 6. Expected Outcome

The completed application provides:

- Request IDs and timestamps.
- End-to-end latency measurements.
- Prompt and generated token counts when reported by Ollama.
- Success and failure tracking.
- Interactive latency and token charts.
- Model performance comparisons.
- SQLite request history and CSV export.

**Important:** End-to-end latency includes application and network overhead. Ollama's generation duration measures the model's generation phase. The dashboard is a local learning implementation, not a fully production-hardened monitoring platform.

### Screenshots

