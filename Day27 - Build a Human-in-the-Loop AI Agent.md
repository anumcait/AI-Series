# 🚀 Day 27 — Build a Human-in-the-Loop AI Agent

## Objective

Build a local AI agent using Python, Ollama, and Llama 3.2 that proposes file organization actions, explains its recommendations, and waits for explicit human approval before executing any action.

The key lesson is:

**An AI recommendation is not permission to execute.**

Python must enforce the approval gate independently of the LLM.

## 1. Technology Stack

- Python
- Ollama
- Llama 3.2
- JSON
- File operations
- Human approval workflow
- Unit testing

## 2. Project Structure

Create the following project:

    day27_agent/
    ├── main.py
    ├── test_agent.py
    ├── requirements.txt
    └── actions.jsonl

File descriptions:

- `main.py` — contains the AI planner, validation, approval workflow, file operations, and logging.
- `test_agent.py` — contains automated tests for approval enforcement and safety.
- `requirements.txt` — lists external Python dependencies.
- `actions.jsonl` — stores the action decisions and execution results. It is created automatically when the program logs an event.

## 3. Install and Configure the Environment

### Step 1: Check Python

Run:

    python --version

Expected result: Python prints its installed version.

### Step 2: Check Ollama

Run:

    ollama --version

Expected result: Ollama prints its version.

### Step 3: Download Llama 3.2

Run:

    ollama pull llama3.2

Expected result: The model is downloaded and available locally.

### Step 4: Test the Model

Run:

    ollama run llama3.2

Type:

    Hello

Confirm that the model responds, then exit using:

    /bye

### Step 5: Create a Virtual Environment

Run:

    python -m venv .venv

Activate it on Windows PowerShell:

    .venv\Scripts\Activate.ps1

Or activate it in Git Bash:

    source .venv/Scripts/activate

### Step 6: Install Dependencies

Create `requirements.txt` with:

    requests

Install the dependency:

    python -m pip install -r requirements.txt

Expected result: The Requests library is installed.

## 4. Define the Agent Workflow

The agent follows this sequence:

1. The user enters a goal.
2. Python collects the available sample filenames.
3. Llama 3.2 proposes a structured JSON action plan.
4. Python validates each proposed action.
5. The application displays the source, destination, and reason.
6. The user explicitly approves, rejects, or cancels.
7. Python executes only approved and validated actions.
8. The application records decisions and outcomes in the audit log.

The LLM must never execute file operations directly.

## 5. Implement the AI Planner

In `main.py`, implement `generate_plan(goal, filenames)`.

The function sends the goal, filenames, and permitted categories to Ollama.

The model must return a JSON object containing an `actions` array.

Example structure:

    {
      "actions": [
        {
          "source": "notes.txt",
          "destination": "Documents/notes.txt",
          "reason": "Text files belong in Documents."
        }
      ]
    }

Allowed categories:

- Documents: `.txt`, `.doc`, `.docx`
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`
- Reports: `.pdf`, `.csv`

The model may propose actions, but its output must always be treated as untrusted input.

If the JSON is malformed or the structure is unexpected, the program must stop planning safely without executing any file operation.

## 6. Create Temporary Sample Files

Implement `create_test_files(folder)`.

Create the following disposable files:

- `notes.txt`
- `photo.jpg`
- `report.pdf`

The files must be placed inside a temporary test directory.

Do not use your actual Downloads folder during development.

Expected result: The test workspace contains sample files that can be safely moved and removed.

## 7. Implement Path Validation

Implement `validate_action(action, test_folder)`.

Validate each action before requesting approval and again immediately before execution.

The validation must check:

- The action is a correctly structured object.
- The source filename is a string and contains no path traversal.
- The source file exists inside the test workspace.
- The destination uses an approved category.
- The destination filename matches the source filename.
- The file extension matches the permitted category.
- Resolved paths remain inside the test workspace.
- The destination does not already exist.
- Unexpected operations and malformed parameters are rejected.

Reject unsafe paths, including paths containing `..`, absolute paths, and paths that escape the allowed directory.

Do not overwrite existing files.

Expected result: Invalid actions are blocked before execution.

## 8. Implement Human Approval

Implement `request_approval(action)`.

Display the proposed source, destination, and reason.

Ask the user to choose:

- `A` — Approve
- `R` — Reject
- `C` — Cancel

Expected behavior:

- Approve: Proceed to the execution function after validation.
- Reject: Log the rejection and do not execute the action.
- Cancel: Log the cancellation and stop processing remaining actions.
- Invalid input: Ask again without executing anything.

Approval must come from explicit human input. A model-generated field such as `"approved": true` must never count as human approval.

## 9. Implement Controlled Execution

Implement `execute_action(action, test_folder)`.

The function must independently validate the action before moving a file.

Only the application's approval workflow should call the execution function.

The execution function must:

1. Validate the action.
2. Resolve the source and destination inside the test workspace.
3. Create the approved destination category if needed.
4. Ensure the destination does not already exist.
5. Move the file.
6. Return a success result or report an error.

Expected result: Approved files move to their intended categories. Rejected files remain untouched.

## 10. Implement Audit Logging

Implement `write_log(action, decision, result, log_path)`.

Append one JSON record per event to `actions.jsonl`.

Each record should include:

- Timestamp
- Source filename
- Destination
- Reason
- Human decision
- Execution result

Example record:

    {
      "source": "notes.txt",
      "destination": "Documents/notes.txt",
      "reason": "Text files belong in Documents.",
      "decision": "rejected",
      "result": "Not executed."
    }

The actual log should contain one JSON object per line.

Record approved, rejected, cancelled, blocked, and failed actions.

Expected result: The log provides a persistent audit trail even after temporary test files are removed.

## 11. Run the Agent

Start Ollama if it is not already running:

    ollama serve

If the server is already running, leave it running.

Start the project:

    python main.py

Enter this goal:

    Organize my sample files into Documents, Images, and Reports.

Review the proposed actions.

Test each decision:

- Approve one action.
- Reject another action.
- Cancel a subsequent workflow.

Expected result:

- Approved actions move the files.
- Rejected actions do not execute.
- Cancellation stops further processing.
- Decisions and outcomes are written to the audit log.
- Temporary test files are removed when the program exits.

## 12. Write Automated Safety Tests

Implement the following tests in `test_agent.py`:

### Test 1: Approved Action

Approve a valid action.

Expected result: The file moves to the destination.

### Test 2: Rejected Action

Reject a valid action.

Expected result: The source file remains in place, and the execution function is never called.

### Test 3: Cancelled Workflow

Cancel a workflow containing multiple actions.

Expected result: No subsequent action is executed.

### Test 4: Path Traversal

Submit a source or destination containing `..`.

Expected result: Validation rejects the action.

### Test 5: Destination Outside the Workspace

Submit an absolute path or an external destination.

Expected result: Validation rejects the action.

### Test 6: Existing Destination

Create a destination file before attempting the move.

Expected result: The action is blocked, and existing content is not overwritten.

### Test 7: Malformed Model Output

Simulate invalid JSON or an invalid plan.

Expected result: The program stops planning safely and performs no file operation.

Run the tests:

    python -m unittest -v

Expected result: All seven tests pass.

## 13. Troubleshooting

### Ollama Returns HTTP 404

Check the installed version:

    ollama --version

Check available models:

    ollama list

Test the server:

    curl http://localhost:11434/

Test the generation endpoint:

    curl -X POST http://localhost:11434/api/generate \
      -H "Content-Type: application/json" \
      -d '{"model":"llama3.2","prompt":"Reply with OK","stream":false}'

The standard Ollama generation endpoint is `/api/generate`.

### The Model Does Not Return the Expected JSON

Ensure the prompt clearly specifies the expected JSON structure.

The Python code should accept only the intended structure, such as an `actions` array, and reject malformed or unexpected output.

Never remove validation or approval checks to solve a formatting issue.

### No File Is Moved

Check that:

- The action passed validation.
- The destination category matches the extension.
- The destination does not already exist.
- The human explicitly approved the action.
- No execution error occurred.

Inspect `actions.jsonl` to understand the recorded outcome.

## Key Learning

An AI recommendation is not permission to execute.

The LLM proposes actions, but Python controls permissions, validates parameters, enforces approval, performs file operations, and records outcomes.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/4bf70bf6-35ab-42b8-bd1e-e23c1c42ceb4" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/4e8bcff9-0d14-4fc0-89bd-765acecd80d2" />


