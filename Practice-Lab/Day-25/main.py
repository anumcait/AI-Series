import json
from ollama import chat

MODEL = "llama3.2:3b"

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