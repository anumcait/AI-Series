import json
import logging
from datetime import datetime
from pathlib import Path

import ollama

MODEL = "llama3.2:3b"
OUTPUT_DIR = Path("runs")
OUTPUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def run_agent(role, instructions, task, previous_output=None):
    """Run one agent and require a JSON response."""
    logging.info("Starting %s agent", role)

    prompt = f"""
You are the {role} agent in a multi-agent workflow.

Your responsibility:
{instructions}

User task:
{task}

Previous agent output:
{json.dumps(previous_output, ensure_ascii=False)}

Return ONLY valid JSON, with no Markdown fences.
Use this structure:
{{
  "agent": "{role}",
  "result": "Your detailed result as a string",
  "gaps": ["Any missing information or limitations"]
}}
"""
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )

    result = json.loads(response["message"]["content"])
    logging.info("Completed %s agent", role)
    return result


def main():
    task = input("Enter your task: ").strip()
    if not task:
        print("Please enter a task and try again.")
        return

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    history = []

    try:
        research = run_agent(
            "Research",
            "Identify essential topics, prerequisites, learning order, "
            "and beginner-friendly resources or practice ideas.",
            task,
        )
        history.append({"stage": "research", "output": research})

        planning = run_agent(
            "Planning",
            "Create a practical, ordered plan with milestones, activities, "
            "and measurable outcomes. Use the research output.",
            task,
            research,
        )
        history.append({"stage": "planning", "output": planning})

        review = run_agent(
            "Reviewer",
            "Check the plan for missing prerequisites, unrealistic pacing, "
            "unclear steps, and missing practice. Improve the plan and "
            "provide the corrected final version.",
            task,
            {"research": research, "plan": planning},
        )
        history.append({"stage": "review", "output": review})

        final_output = {
            "task": task,
            "research": research,
            "plan": planning,
            "reviewed_result": review,
        }

        print("\n=== FINAL REVIEWED OUTPUT ===")
        print(review["result"])

    except Exception as error:
        logging.exception("Workflow failed")
        history.append({
            "stage": "failure",
            "error": str(error),
        })
        print(f"\nWorkflow failed: {error}")
        print("Check that Ollama is running and the model is installed.")

    finally:
        log_file = OUTPUT_DIR / f"run_{run_id}.json"
        log_file.write_text(
            json.dumps(history, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"\nExecution log saved to: {log_file}")


if __name__ == "__main__":
    main()