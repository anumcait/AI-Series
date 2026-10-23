import json
import re
import time
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "test_cases.json"
OLLAMA_URL = "http://localhost:11434/api/generate"


def load_cases():
    with open(DATA_FILE, encoding="utf-8") as file:
        return json.load(file)


def call_ollama(model, prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0}
        },
        timeout=180
    )
    response.raise_for_status()
    return response.json()["response"].strip()


def evaluate_answer(case, answer):
    """Transparent heuristic scores, each from 0 to 100."""
    answer_lower = answer.lower()
    required = case.get("must_include", [])

    # Completeness: coverage of required terms.
    completeness = (
        100 * sum(term.lower() in answer_lower for term in required)
        / len(required)
        if required else 100
    )

    # Relevance: overlap between meaningful question words and answer words.
    stopwords = {
        "what", "is", "the", "a", "an", "in", "on", "to", "for",
        "how", "many", "does", "do", "according", "supplied",
        "context", "write", "that", "two", "and", "their"
    }
    question_words = {
        word for word in re.findall(r"\b\w+\b", case["question"].lower())
        if len(word) > 2 and word not in stopwords
    }
    answer_words = set(re.findall(r"\b\w+\b", answer_lower))
    relevance = (
        100 * len(question_words & answer_words) / len(question_words)
        if question_words else 100
    )

    # Clarity: a simple length and sentence-structure proxy, not a
    # genuine understanding of writing quality.
    words = answer.split()
    sentences = [s for s in re.split(r"[.!?]+", answer) if s.strip()]
    clarity = 100 if 8 <= len(words) <= 120 and 1 <= len(sentences) <= 6 else 60
    if not answer.strip():
        clarity = 0

    # Instruction following: checks the requested output type.
    fmt = case.get("expected_format", "paragraph")
    if fmt == "code":
        instruction = 100 if "def " in answer and "return" in answer else 0
    elif fmt == "paragraph":
        instruction = 100 if len(words) <= 120 else 50
    else:
        instruction = 100

    # Groundedness: checks overlap with context when provided.
    # This is a lexical proxy, NOT proof that every claim is supported.
    context = case.get("context", "").lower()
    if context:
        context_words = set(re.findall(r"\b\w+\b", context))
        answer_content = {
            word for word in answer_words
            if len(word) > 3 and word not in stopwords
        }
        groundedness = (
            100 * len(answer_content & context_words) / len(answer_content)
            if answer_content else 0
        )
    else:
        groundedness = None

    scores = {
        "relevance": round(relevance),
        "completeness": round(completeness),
        "clarity": round(clarity),
        "instruction_following": round(instruction),
    }

    if groundedness is not None:
        scores["groundedness"] = round(groundedness)

    overall = round(sum(scores.values()) / len(scores))
    passed = overall >= 70 and completeness >= 50 and instruction >= 50

    return {
        **scores,
        "overall": overall,
        "passed": passed,
        "answer": answer
    }


def build_prompt(case, instruction):
    context = case.get("context", "")
    return (
        f"{instruction}\n\n"
        f"Reference context (use when relevant):\n{context or 'Not provided'}\n\n"
        f"Question: {case['question']}\n"
        "Answer the question directly."
    )


st.set_page_config(page_title="Day 32 AI Evaluator", layout="wide")
st.title("🧪 Day 32 — Local AI Evaluation Framework")
st.caption("Run repeatable tests, inspect failures, compare prompts, and export reports.")

try:
    cases = load_cases()
except (OSError, json.JSONDecodeError) as error:
    st.error(f"Cannot load test_cases.json: {error}")
    st.stop()

with st.sidebar:
    st.header("Configuration")
    model = st.text_input("Ollama model", "qwen3:4b")
    st.caption("The model must already be available in Ollama.")
    st.write(f"Test cases loaded: {len(cases)}")

tab_run, tab_compare, tab_history = st.tabs(
    ["Run evaluation", "Compare prompts", "Results"]
)

if "results" not in st.session_state:
    st.session_state.results = []

with tab_run:
    st.subheader("Run the test suite")
    prompt = st.text_area(
        "System prompt",
        "You are a helpful technical assistant. Give accurate, concise answers.",
        height=100
    )

    if st.button("▶ Run all tests", type="primary"):
        progress = st.progress(0)
        status = st.status("Starting evaluation...", expanded=True)
        run_results = []
        start = time.time()

        try:
            for index, case in enumerate(cases):
                status.write(f"Running {case['id']}: {case['question']}")
                answer = call_ollama(
                    model, build_prompt(case, prompt)
                )
                scored = evaluate_answer(case, answer)
                run_results.append({
                    "test_id": case["id"],
                    "question": case["question"],
                    "prompt_name": "Prompt A",
                    "latency_seconds": round(time.time() - start, 2),
                    **scored
                })
                progress.progress((index + 1) / len(cases))

            st.session_state.results = run_results
            status.update(label="Evaluation complete", state="complete")
            st.success(f"Completed {len(run_results)} test cases.")

        except requests.RequestException as error:
            status.update(label="Evaluation failed", state="error")
            st.error(
                f"Could not reach Ollama: {error}. "
                "Check that Ollama is running and the model is installed."
            )

    if st.session_state.results:
        df = pd.DataFrame(st.session_state.results)
        st.dataframe(df, use_container_width=True)
        st.metric("Average score", f"{df['overall'].mean():.1f}/100")
        st.metric("Pass rate", f"{100 * df['passed'].mean():.0f}%")

        st.download_button(
            "Download JSON report",
            json.dumps(st.session_state.results, indent=2),
            "evaluation_report.json",
            "application/json"
        )
        st.download_button(
            "Download CSV report",
            df.to_csv(index=False),
            "evaluation_report.csv",
            "text/csv"
        )

with tab_compare:
    st.subheader("Compare two system prompts")
    prompt_a = st.text_area(
        "Prompt A",
        "You are a helpful technical assistant. Answer accurately.",
        key="prompt_a"
    )
    prompt_b = st.text_area(
        "Prompt B",
        "You are a technical tutor. Answer directly, include required details, "
        "and use code when asked for code.",
        key="prompt_b"
    )

    if st.button("⚖ Compare prompts"):
        comparison = []
        progress = st.progress(0)
        status = st.status("Comparing prompts...", expanded=True)
        total = len(cases) * 2
        completed = 0

        try:
            for label, instruction in [
                ("Prompt A", prompt_a), ("Prompt B", prompt_b)
            ]:
                for case in cases:
                    status.write(f"{label} — {case['id']}")
                    answer = call_ollama(
                        model, build_prompt(case, instruction)
                    )
                    scored = evaluate_answer(case, answer)
                    comparison.append({
                        "test_id": case["id"],
                        "prompt_name": label,
                        "overall": scored["overall"],
                        "passed": scored["passed"],
                        "answer": scored["answer"],
                        "relevance": scored["relevance"],
                        "completeness": scored["completeness"],
                        "clarity": scored["clarity"],
                        "instruction_following": scored[
                            "instruction_following"
                        ],
                        "groundedness": scored.get("groundedness")
                    })
                    completed += 1
                    progress.progress(completed / total)

            result_df = pd.DataFrame(comparison)
            st.session_state.comparison = comparison
            st.dataframe(result_df, use_container_width=True)
            summary = result_df.groupby("prompt_name")["overall"].mean()
            st.bar_chart(summary)
            st.success("Comparison complete.")

        except requests.RequestException as error:
            status.update(label="Comparison failed", state="error")
            st.error(f"Ollama request failed: {error}")

    if st.session_state.get("comparison"):
        comparison_df = pd.DataFrame(st.session_state.comparison)
        st.download_button(
            "Download comparison CSV",
            comparison_df.to_csv(index=False),
            "prompt_comparison.csv",
            "text/csv"
        )

with tab_history:
    st.subheader("Inspect the latest single-prompt run")
    if st.session_state.results:
        history_df = pd.DataFrame(st.session_state.results)
        st.dataframe(
            history_df[history_df["passed"] == False],
            use_container_width=True
        )
        st.caption("An empty table means no tests failed the current threshold.")
    else:
        st.info("Run an evaluation first to see results here.")