Writing

# 🚀 Day 25 — AI Planning and Task Decomposition 🧠

- Build a local AI agent that breaks a complex goal into ordered steps, validates its plan, and tracks task completion.

## 1\. Project Overview

Build a local AI planning agent using Python, Ollama, and Llama 3.2. The agent takes a goal, creates a structured plan, validates the plan, displays tasks in order, and tracks completion.

## 2\. Problem Statement

Complex goals can be difficult to complete without a clear plan. An AI model can suggest steps, but its output may contain missing fields, invalid task IDs, or poorly structured data.

This project addresses these problems by combining AI-generated plans with Python validation and progress tracking.

## 3\. Learning Objectives

- Understand AI planning and task decomposition.
- Generate structured JSON output from an LLM.
- Validate AI-generated plans using Python.
- Track task completion using Boolean values.
- Save a plan and its progress to a JSON file.
- Handle common errors during AI execution.

## 4\. Tools and Technologies

- **Python:** Main programming language.
- **Ollama:** Runs the language model locally.
- **Llama 3.2:** Generates the task plan.
- **JSON:** Stores structured plans and task status.
- **VS Code:** Development environment.

## 5\. Project Setup

### Step 1: Create the project folder

Open the VS Code terminal and run:

```
cd D:\AI-Series\Practice-Lab
mkdir Day-25
cd Day-25
code .
```

If your project is stored elsewhere, replace the path with your actual `Practice-Lab` location.

**Expected result:** A new `Day-25` folder opens in VS Code.

### Step 2: Check Python and Ollama

Run:

```
python --version
ollama --version
```

If Ollama is not installed, install it from https://ollama.com/.

Download the model:

```
ollama pull llama3.2
```

**Why:** Python runs the agent, while Ollama provides the local language model.

### Step 3: Create a virtual environment

Run:

```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Install the dependency:

```
pip install ollama
```

Create `requirements.txt` with this content:

```
ollama
```

**Expected result:** The virtual environment is activated, and the Ollama Python package is installed.

## 6\. Implement the AI Planning Agent

### Step 1: Create `main.py`

Create a new file named `main.py` inside `Day-25` and add the following code:

```
import json
from ollama import chat

MODEL = "llama3.2"

def create_plan(goal):
    response = chat(
        model=MODEL,
        format="json",
        messages=[
            {
                "role": "system",
                "content": """
You are a project planning assistant.
Break the user's goal into 3 to 7 ordered tasks.
Return ONLY a JSON object with this structure:
{
  "goal": "the original goal",
  "tasks": [
    {
      "id": 1,
      "title": "short task title",
      "description": "what to do",
      "done": false
    }
  ]
}
Use consecutive task IDs starting at 1.
Put tasks in dependency order.
Keep tasks practical and achievable.
"""
            },
            {"role": "user", "content": goal}
        ]
    )

    return json.loads(response.message.content)

def validate_plan(plan):
    if not isinstance(plan, dict):
        return False, "Plan must be a JSON object."

    if not isinstance(plan.get("goal"), str) or not plan["goal"].strip():
        return False, "Plan must have a non-empty goal."

    tasks = plan.get("tasks")

    if not isinstance(tasks, list) or not 3 <= len(tasks) <= 7:
        return False, "Plan must contain between 3 and 7 tasks."

    required = {"id", "title", "description", "done"}

    for index, task in enumerate(tasks, start=1):
        if not isinstance(task, dict) or not required.issubset(task):
            return False, f"Task {index} has missing fields."

        if task["id"] != index:
            return False, "Task IDs must be consecutive, starting at 1."

        if not isinstance(task["title"], str) or not task["title"].strip():
            return False, f"Task {index} has an invalid title."

        if not isinstance(task["description"], str):
            return False, f"Task {index} has an invalid description."

        if not isinstance(task["done"], bool):
            return False, f"Task {index} must have a Boolean done value."

    return True, "Plan is valid."

def show_plan(plan):
    print(f"\nGOAL: {plan['goal']}\n")

    for task in plan["tasks"]:
        status = "DONE" if task["done"] else "PENDING"
        print(f"{task['id']}. [{status}] {task['title']}")
        print(f"   {task['description']}")

def track_progress(plan):
    for task in plan["tasks"]:
        if task["done"]:
            continue

        answer = input(
            f"\nMark task {task['id']} complete? "
            f"({task['title']}) [y/n/q]: "
        ).strip().lower()

        if answer == "q":
            break

        if answer == "y":
            task["done"] = True

    completed = sum(task["done"] for task in plan["tasks"])
    total = len(plan["tasks"])

    print(f"\nProgress: {completed}/{total} tasks completed.")

    if completed == total:
        print("All tasks completed!")
    else:
        print("Remaining tasks are still pending.")

    with open("plan.json", "w", encoding="utf-8") as file:
        json.dump(plan, file, indent=2, ensure_ascii=False)

    print("Plan saved to plan.json")

def main():
    goal = input(
        "Enter your project goal "
        "(press Enter for the sample): "
    ).strip()

    if not goal:
        goal = "Complete a beginner Python learning project in 7 days."

    print("\nCreating your plan...")

    try:
        plan = create_plan(goal)
    except Exception as error:
        print(f"Could not generate plan: {error}")
        return

    valid, message = validate_plan(plan)
    print(f"\nValidation: {message}")

    if not valid:
        print("Plan rejected. Please try generating it again.")
        return

    show_plan(plan)
    track_progress(plan)

if __name__ == "__main__":
    main()
```

### Step 2: Understand the main functions

- **`create_plan()`** — Sends the goal to Llama 3.2 and converts the JSON response into a Python dictionary.
- **`validate_plan()`** — Checks that the plan contains 3–7 tasks, required fields, consecutive IDs, valid titles, descriptions, and Boolean completion values.
- **`show_plan()`** — Displays the goal and tasks with their current status.
- **`track_progress()`** — Lets the user mark tasks complete or leave them pending.
- **`main()`** — Connects the entire workflow and handles errors during plan generation.

**Important:** Structural validation does not guarantee that the AI's plan is factually correct or that the order is sensible. Review the tasks before executing them.

## 7\. Run the Agent

### Step 1: Check that the model is available

Run:

```
ollama list
```

Confirm that `llama3.2` appears in the list.

### Step 2: Execute the program

Run:

```
python main.py
```

When prompted for a goal, press Enter to use the default:

`Complete a beginner Python learning project in 7 days.`

You can also enter your own goal, such as:

`Organize a small technical workshop in one week.`

### Step 3: Review the generated plan

The agent should generate 3–7 ordered tasks and display a validation message.

Example of the expected format:

```
Validation: Plan is valid.

GOAL: Complete a beginner Python learning project in 7 days.

1. [PENDING] Review Python basics
   Practice variables, data types, and control flow.
2. [PENDING] Learn functions
   Create reusable functions and test them.
3. [PENDING] Build a small project
   Apply the concepts in a simple Python application.
```

The actual tasks will be generated by the model and may differ from this example.

## 8\. Track Task Completion

For each task, the agent asks:

```
Mark task 1 complete? (Review Python basics) [y/n/q]:
```

- Enter `y` to mark the task complete.
- Enter `n` to leave it pending.
- Enter `q` to stop tracking the remaining tasks.

After tracking, the program displays the completion count and saves the plan to `plan.json`.

Example:

```
Progress: 1/3 tasks completed.
Remaining tasks are still pending.
Plan saved to plan.json
```

Open `plan.json` in VS Code to inspect the saved goal, task descriptions, IDs, and completion status.

**Current limitation:** This version creates a new plan every time it runs. It saves progress but does not reload an existing plan, automatically enforce task dependencies, or execute tasks on the user's behalf.

## 9\. Testing and Validation

Complete these three tests.

### Test 1: Plan generation

Run `python main.py` and press Enter at the goal prompt.

**Expected result:** The AI generates a plan, and validation succeeds.

### Test 2: Completion tracking

Enter `y` for one task and `n` for another.

Open `plan.json`.

**Expected result:** The completed task has `"done": true`, while the pending task has `"done": false`.

### Test 3: Quit behavior

Run the program again and enter `q` at the first task prompt.

**Expected result:** The program stops asking about the remaining tasks and saves the current plan without marking the first task complete.

## 10\. Common Errors and Solutions

- **Ollama connection error:** Make sure Ollama is installed and running, then retry.
- **Model not found:** Run `ollama pull llama3.2`.
- **Python package not found:** Activate the virtual environment and run `pip install -r requirements.txt`.
- **PowerShell activation error:** Use the process-scoped execution policy command shown in the setup section.
- **Plan validation fails:** Run the program again. The model may have returned data that does not meet the expected structure.
- **JSON parsing error:** Confirm that Ollama returned valid JSON. The current program reports the error but does not automatically repair malformed output.

## 11\. Key Concepts Learned

- **Planning:** Converting a large goal into manageable tasks.
- **Task decomposition:** Dividing a goal into smaller steps.
- **Structured outputs:** Using JSON to represent a plan consistently.
- **Validation:** Checking AI-generated data before using it.
- **Execution control:** Allowing a user to control task completion.
- **Progress tracking:** Recording which tasks are complete.
- **Persistence:** Saving the plan and status to a file.

## 12\. Final Checklist

- [ ]Created the `Day-25` folder.
- [ ]Set up Python and Ollama.
- [ ]Installed the required dependency.
- [ ]Created `main.py`.
- [ ]Generated a plan using the local model.
- [ ]Validated the generated plan.
- [ ]Tested task completion and quit behavior.
- [ ]Verified that `plan.json` was created.
- [ ]Recorded the results and any errors.

## 13\. Conclusion

Day 25 demonstrates how to build a basic AI planning agent that decomposes a goal, returns structured tasks, validates its output, and tracks completion.

The agent combines language-model reasoning with deterministic Python checks. This is a useful foundation for more advanced agents that reload saved plans, enforce task dependencies, retry invalid plans, and execute approved actions.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/8e23af85-e1e2-462d-8916-dd7c87c3fb62" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/0cd2e53d-fe99-4393-9cb2-c863ea2d4026" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/6057ccc8-64ec-4a19-a42d-663800edfdbc" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/7fdd8a85-bb9e-4c4e-98cb-81d76054fbb9" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/f6242e57-d8ac-4665-a8a8-25451c984789" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/798e65b2-75d9-4df5-be4b-78e6ca5e48f7" />






