import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import requests


MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

ALLOWED_CATEGORIES = {
    ".txt": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".pdf": "Reports",
    ".csv": "Reports",
}


def create_test_files(folder):
    """Create disposable sample files inside the test folder."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    samples = {
        "notes.txt": "Sample notes for Day 27.",
        "photo.jpg": "Fake image data for testing.",
        "report.pdf": "Fake PDF data for testing.",
    }

    for filename, content in samples.items():
        path = folder / filename
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    return list(samples.keys())


def generate_plan(goal, filenames):
    """Ask the local Llama model for a JSON action plan."""

    prompt = f"""
You are a file organization planning assistant.

User goal: {goal}

Files available:
{json.dumps(filenames)}

Allowed categories:
- Documents: .txt, .doc, .docx
- Images: .jpg, .jpeg, .png, .gif
- Reports: .pdf, .csv

Return ONLY a JSON object containing an "actions" array.

Each action must have:
- source: an existing filename from the supplied list
- destination: Category/filename
- reason: a short explanation

Example output:
{{
  "actions": [
    {{
      "source": "notes.txt",
      "destination": "Documents/notes.txt",
      "reason": "Text files belong in Documents."
    }}
  ]
}}

Rules:
- Use only the supplied filenames.
- Preserve the original filename.
- Use only the allowed categories.
- Do not propose deletion or any other operation.
- Do not include Markdown code fences.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        },
        timeout=120,
    )
    response.raise_for_status()

    answer = response.json()["response"]
    data = json.loads(answer)

    if isinstance(data, dict) and isinstance(data.get("actions"), list):
        plan = data["actions"]
    elif isinstance(data, list):
        plan = data
    else:
        raise ValueError(
            "The model did not return an actions array. "
            f"Output: {answer[:500]}"
        )

    return plan


def validate_action(action, test_folder):
    """
    Return (True, message) only when the proposed move is safe.
    Never trust paths merely because they came from the model.
    """
    if not isinstance(action, dict):
        return False, "Action must be a JSON object."

    required = {"source", "destination", "reason"}
    if not required.issubset(action):
        return False, "Action is missing required fields."

    source_name = action["source"]
    destination_name = action["destination"]

    if not isinstance(source_name, str) or not isinstance(
        destination_name, str
    ):
        return False, "Source and destination must be strings."

    if not isinstance(action["reason"], str):
        return False, "Reason must be a string."

    # Source must be a single filename, not a path.
    if (
        not source_name
        or Path(source_name).name != source_name
        or source_name in {".", ".."}
        or "/" in source_name
        or "\\" in source_name
    ):
        return False, "Unsafe source filename."

    # Destination must be exactly Category/filename.
    parts = destination_name.replace("\\", "/").split("/")
    if len(parts) != 2 or any(part in {"", ".", ".."} for part in parts):
        return False, "Destination must be Category/filename."

    category, destination_file = parts

    if category not in {"Documents", "Images", "Reports"}:
        return False, "Destination category is not allowed."

    if destination_file != source_name:
        return False, "Changing filenames is not allowed."

    expected_category = ALLOWED_CATEGORIES.get(
        Path(source_name).suffix.lower()
    )
    if expected_category != category:
        return False, "Category does not match the file type."

    root = Path(test_folder).resolve()
    source = (root / source_name).resolve()
    destination_dir = (root / category).resolve()
    destination = (root / category / destination_file).resolve()

    # Check resolved paths, including paths affected by symlinks.
    if not source.is_relative_to(root):
        return False, "Source escapes the test folder."

    if not destination_dir.is_relative_to(root):
        return False, "Destination escapes the test folder."

    if not destination.is_relative_to(root):
        return False, "Destination escapes the test folder."

    if not source.is_file():
        return False, "Source file does not exist."

    if destination.exists():
        return False, "Destination already exists; overwrite blocked."

    return True, "Action passed validation."


def execute_action(action, test_folder):
    """Move one file only after a fresh safety validation."""
    valid, message = validate_action(action, test_folder)

    if not valid:
        raise ValueError(message)

    root = Path(test_folder).resolve()
    source = root / action["source"]
    category = action["destination"].split("/")[0]
    destination_dir = root / category

    destination_dir.mkdir(exist_ok=True)

    # Revalidate immediately before moving.
    valid, message = validate_action(action, test_folder)
    if not valid:
        raise ValueError(message)

    shutil.move(str(source), str(destination_dir / source.name))
    return "executed"


def request_approval(action, input_fn=input):
    """Ask the human to approve, reject, or cancel."""
    print("\nProposed action")
    print(f"  Source:      {action.get('source')}")
    print(f"  Destination: {action.get('destination')}")
    print(f"  Reason:      {action.get('reason')}")

    while True:
        choice = input_fn(
            "Choose [A]pprove, [R]eject, or [C]ancel: "
        ).strip().lower()

        if choice in {"a", "r", "c"}:
            return {"a": "approved", "r": "rejected", "c": "cancelled"}[
                choice
            ]

        print("Invalid choice. Enter A, R, or C.")


def write_log(action, decision, result, log_path):
    """Append an audit record without overwriting earlier records."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": action.get("source") if isinstance(action, dict) else None,
        "destination": (
            action.get("destination") if isinstance(action, dict) else None
        ),
        "reason": action.get("reason") if isinstance(action, dict) else None,
        "decision": decision,
        "result": result,
    }

    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


def run_workflow(
    goal,
    test_folder,
    log_path,
    input_fn=input,
    planner=generate_plan,
):
    """Plan, validate, request approval, and execute approved moves."""
    filenames = [
        path.name
        for path in Path(test_folder).iterdir()
        if path.is_file()
    ]

    try:
        plan = planner(goal, filenames)
    except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
        print(f"Could not generate a valid plan: {exc}")
        write_log({}, "error", f"Planning failed: {exc}", log_path)
        return

    if not isinstance(plan, list):
        print("Invalid plan: expected a JSON array.")
        write_log({}, "error", "Plan was not a list.", log_path)
        return

    for action in plan:
        valid, message = validate_action(action, test_folder)

        if not valid:
            print(f"\nAction blocked: {message}")
            write_log(action, "rejected_by_validator", message, log_path)
            continue

        decision = request_approval(action, input_fn)

        if decision == "cancelled":
            write_log(action, "cancelled", "Not executed.", log_path)
            print("Workflow cancelled. No further actions will run.")
            break

        if decision == "rejected":
            write_log(action, "rejected", "Not executed.", log_path)
            print("Action rejected. No file was moved.")
            continue

        # Only the explicit human approval reaches this branch.
        # Validate again inside execute_action before moving.
        try:
            result = execute_action(action, test_folder)
            write_log(action, "approved", result, log_path)
            print(f"Success: {action['source']} was moved.")
        except (OSError, ValueError, shutil.Error) as exc:
            write_log(action, "approved", f"Execution failed: {exc}", log_path)
            print(f"Execution failed: {exc}")


def main():
    # The test workspace is temporary and automatically removed on exit.
    # Nothing in your real Downloads folder is accessed.
    project_dir = Path(__file__).resolve().parent
    log_path = project_dir / "actions.jsonl"

    with tempfile.TemporaryDirectory(prefix="day27_test_") as temp:
        test_folder = Path(temp)
        create_test_files(test_folder)

        print("Day 27 Human-in-the-Loop Agent")
        print(f"Temporary test folder: {test_folder}")
        print("Sample files:", ", ".join(
            path.name for path in test_folder.iterdir()
        ))

        goal = input("\nEnter your goal: ").strip()
        if not goal:
            print("No goal provided. Exiting safely.")
            return

        run_workflow(goal, test_folder, log_path)

        print("\nRemaining files in the test folder:")
        for path in sorted(test_folder.rglob("*")):
            if path.is_file():
                print(f"  {path.relative_to(test_folder)}")

    print(f"\nAudit log saved to: {log_path}")
    print("Temporary test files have been removed.")


if __name__ == "__main__":
    main()