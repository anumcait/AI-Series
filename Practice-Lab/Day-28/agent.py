import json
from datetime import datetime, timezone
from pathlib import Path

import requests

MODEL = "llama3.2:3b"
API_URL = "http://localhost:11434/api/chat"
MAX_RETRIES = 2
PASS_SCORE = 16
REPORT_FILE = Path("evaluations.json")


def ask_model(prompt, json_mode=False):
    """Send a prompt to the local Ollama model."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.2},
    }

    if json_mode:
        payload["format"] = "json"

    response = requests.post(API_URL, json=payload, timeout=180)
    response.raise_for_status()
    return response.json()["message"]["content"]


def evaluate(task, draft):
    """Score the draft against four quality criteria."""
    prompt = f"""
Evaluate the answer against the user's task.

TASK:
{task}

ANSWER:
{draft}

Return ONLY valid JSON with this exact structure:
{{
  "relevance": 1,
  "completeness": 1,
  "clarity": 1,
  "format": 1,
  "strengths": ["specific strength"],
  "weaknesses": ["specific weakness"],
  "improvements": ["specific change needed"]
}}

Score each criterion from 1 to 5:
- relevance: answers the actual task
- completeness: covers the important details
- clarity: easy to understand
- format: follows the user's requested format

Use 5 for excellent and 1 for poor. Be critical and specific.
Do not reward an answer merely for sounding confident.
"""
    result = json.loads(ask_model(prompt, json_mode=True))

    for key in ("relevance", "completeness", "clarity", "format"):
        if type(result.get(key)) is not int or not 1 <= result[key] <= 5:
            raise ValueError(f"Invalid score for {key}")

    for key in ("strengths", "weaknesses", "improvements"):
        if not isinstance(result.get(key), list):
            raise ValueError(f"Invalid list for {key}")

    return result


def improve(task, draft, report):
    """Revise the answer using the evaluation feedback."""
    prompt = f"""
Improve the answer to satisfy the user's original task.

USER TASK:
{task}

CURRENT ANSWER:
{draft}

EVALUATION:
{json.dumps(report, indent=2)}

Address the weaknesses and requested improvements.
Preserve correct information. Do not invent facts.
Return only the improved answer, not your analysis or scorecard.
"""
    return ask_model(prompt).strip()


def run_agent(task):
    draft = ask_model(
        f"Complete this task clearly and accurately:\n{task}"
    ).strip()
    initial_draft = draft
    history = []

    for attempt in range(MAX_RETRIES + 1):
        report = evaluate(task, draft)
        total = sum(
            report[key]
            for key in ("relevance", "completeness", "clarity", "format")
        )

        history.append({
            "attempt": attempt,
            "answer": draft,
            "scores": report,
            "total_score": total,
        })

        if total >= PASS_SCORE or attempt == MAX_RETRIES:
            break

        draft = improve(task, draft, report)

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "task": task,
        "initial_answer": initial_draft,
        "final_answer": draft,
        "initial_scorecard": history[0]["scores"],
        "final_scorecard": history[-1]["scores"],
        "initial_total": history[0]["total_score"],
        "final_total": history[-1]["total_score"],
        "attempts_used": len(history) - 1,
        "history": history,
    }

    reports = []
    if REPORT_FILE.exists():
        reports = json.loads(REPORT_FILE.read_text(encoding="utf-8"))
        if not isinstance(reports, list):
            raise ValueError("Evaluation file must contain a JSON list")

    reports.append(result)
    REPORT_FILE.write_text(
        json.dumps(reports, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n--- INITIAL ANSWER ---\n", initial_draft)
    print("\n--- FINAL ANSWER ---\n", draft)
    print("\n--- FINAL SCORECARD ---")
    print(json.dumps(result["final_scorecard"], indent=2))
    print(f"\nTotal score: {result['final_total']}/20")
    print(f"Improvements used: {result['attempts_used']}")
    print(f"Report saved to: {REPORT_FILE.resolve()}")


if __name__ == "__main__":
    task = input("Enter your task: ").strip()
    if not task:
        raise SystemExit("Please enter a non-empty task.")

    try:
        run_agent(task)
    except (requests.RequestException, ValueError, KeyError,
            TypeError, json.JSONDecodeError) as error:
        raise SystemExit(f"Agent failed: {error}") from error