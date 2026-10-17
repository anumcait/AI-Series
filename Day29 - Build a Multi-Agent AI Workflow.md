# Day 29 — Build a Multi-Agent AI Workflow

## Objective
Build a local multi-agent AI workflow using Python, Ollama, and Llama 3.2. Three specialized agents collaborate to complete a task: Research, Planning, and Reviewer.

## Tech Stack
- Python
- Ollama
- Llama 3.2:3b
- JSON
- Prompt Engineering

## Step 1: Install and Verify Ollama

Install Ollama from https://ollama.com/download.

Download the model:

```bash
ollama pull llama3.2
````

Verify installation:

bash
```
ollama list
```

Test the model:

bash
```
ollama run llama3.2
```

Enter a test prompt and confirm that the model responds. Type `/bye` to exit.

## Step 2: Create the Project

bash
```
mkdir day29
cd day29
python -m venv .venv
```

Activate the virtual environment.

Windows PowerShell:

powershell
```
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

bash
```
source .venv/bin/activate
```

Install the Ollama Python library:

bash
```
python -m pip install ollama
```

## Step 3: Create main.py

Create a file named `main.py` and add the following code:

python
```
import json
import logging
from datetime import datetime
from pathlib import Path

import ollama

MODEL = "llama3.2"
OUTPUT_DIR = Path("runs")
OUTPUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def run_agent(role, instructions, task, previous_output=None):
    logging.info("Starting %s agent", role)

    prompt = f"""
You are the {role} agent in a multi-agent workflow.

Your responsibility:
{instructions}

User task:
{task}

Previous agent output:
{json.dumps(previous_output, ensure_ascii=False)}

Return ONLY valid JSON, without Markdown fences.
Use this structure:
{{
  "agent": "{role}",
  "result": "Your detailed result as a string",
  "gaps": ["Missing information or limitations"]
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
        history.append({
            "stage": "research",
            "output": research,
        })

        planning = run_agent(
            "Planning",
            "Create a practical, ordered plan with milestones, activities, "
            "and measurable outcomes. Use the research output.",
            task,
            research,
        )
        history.append({
            "stage": "planning",
            "output": planning,
        })

        review = run_agent(
            "Reviewer",
            "Check the plan for missing prerequisites, unrealistic pacing, "
            "unclear steps, and missing practice. Improve the plan and "
            "provide the corrected final version.",
            task,
            {"research": research, "plan": planning},
        )
        history.append({
            "stage": "review",
            "output": review,
        })

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


## Step 4: Run the Workflow

Make sure Ollama is running and the virtual environment is activated.

Execute:

bash
```
python main.py
```

Enter the task:

text
```
Prepare a beginner-friendly AI learning plan for 30 days.
Assume the learner knows basic Python but is new to AI.
Include daily topics, hands-on exercises, and a final project.
```

## Step 5: Understand the Workflow

1. Research Agent: Identifies topics, prerequisites, and practice ideas.
2. Planning Agent: Receives the research output and creates an ordered learning plan.
3. Reviewer Agent: Receives the research and plan, checks for gaps, and improves the result.
4. Final Output: Displays the reviewer's result in the terminal.
5. Execution Log: Saves the stage outputs to a JSON file inside the `runs/` directory.

Python controls the agent sequence and passes outputs between stages. Ollama runs Llama 3.2 locally.

## Step 6: Verify Completion

- Ollama responds successfully.
- All three agents execute.
- The final reviewed result appears in the terminal.
- A JSON execution log is created in `runs/`.

## How Real-Time Execution Works

Python sends requests to Ollama's local API. Ollama generates each response, and Python passes the output to the next agent. The stages execute sequentially, with progress logged in the terminal.

This basic workflow does not stream partial tokens or automatically search the internet.

## Outcome

Built a working multi-agent workflow with role-based agents, JSON handoffs, sequential execution, error handling, and execution logging.

Key Learning: Unlike a single self-critiquing agent, this workflow coordinates multiple specialized roles to produce a reviewed result.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/d9aba084-34fe-4b02-bc9a-f8bdb3e7456f" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/6ca0a91b-b0af-4111-b31c-8abfe6e485f7" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/be52837d-0d7e-461c-a1d4-28743081674e" />





