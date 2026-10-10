# Day 23 — Build a Multi-Tool AI DevOps Agent

## 1\. Project Overview

### Objective

Build a Multi-Tool AI DevOps Agent using Python, Ollama, and Llama 3.2. The agent will investigate a simulated server environment by selecting and coordinating multiple tools, evaluating their results, and deciding whether additional investigation is necessary.

This project builds on the tool-calling and AI-agent concepts from previous work while focusing on multi-tool orchestration, conditional execution, result aggregation, and reliable error handling.

### Problem Statement

A DevOps engineer may ask:

> Investigate the server and tell me whether it is healthy.

Instead of running a single function, the agent should coordinate several diagnostic tools, identify potential problems, investigate relevant logs, and produce a consolidated report.

### Project Scope

- Use simulated server data.
- Keep diagnostic functions separate from agent orchestration.
- Register tools and execute them through a controlled dispatcher.
- Support conditional investigation.
- Handle invalid tools, invalid arguments, and execution failures.
- Use Ollama with Llama 3.2 for model-driven tool selection.
- Run the application through a command-line interface.
- Do not connect to or modify real servers.

---

## 2\. Expected Project Structure

The Day-23 project is maintained independently inside the `Practice-Lab/Day-23` directory.

```
Day-23/
├── app.py
├── models.py
├── requirements.txt
├── test_tools.py
└── tools.py
```

The project may also use the existing virtual environment at the `Practice-Lab` level.

### File Responsibilities

| File | Responsibility |
| --- | --- |
| `app.py` | Main application, orchestration, conditional execution, and consolidated reporting |
| `tools.py` | Diagnostic functions, tool registration, dispatcher, validation, and serialization |
| `models.py` | Model configuration and interaction with Ollama |
| `requirements.txt` | Python dependencies |
| `test_tools.py` | Tests for tool execution, validation, and error handling |

Each module should have one clear responsibility. The model should decide which tool to call, while Python functions should perform the actual simulated checks.

---

## 3\. Technology Stack

| Component | Technology |
| --- | --- |
| Programming language | Python |
| Local language model | Ollama with Llama 3.2 |
| Tool execution | Custom Python functions |
| Tool arguments and results | JSON-compatible data |
| Interface | Command line |
| Development environment | Windows with VS Code |
| Server data | Simulated |
| Testing | Python test scripts |

---

## 4\. Available Diagnostic Tools

### Tool 1 — Server Health

**Function:** `check_server_health()`

Purpose:

- Check simulated server availability.
- Return the current simulated health status.
- Provide structured output that the agent can interpret.

Example result:

```
{
  "ok": true,
  "status": "healthy",
  "message": "Simulated server is responding."
}
```

The exact field names and values should match the implementation in `tools.py`.

### Tool 2 — Resource Monitor

**Function:** `monitor_resources()`

Purpose:

- Inspect simulated CPU utilization.
- Inspect memory utilization.
- Inspect disk utilization.
- Identify resource warnings.

Illustrative result:

```
{
  "ok": true,
  "cpu_percent": 35,
  "memory_percent": 61,
  "disk_percent": 92
}
```

These readings are examples, not real server measurements.

The orchestration logic should use explicit numeric thresholds rather than relying solely on searching the output for warning-related words.

### Tool 3 — Service Checker

**Function:** `check_services()`

Purpose:

- Check simulated Nginx status.
- Check simulated Tomcat status.
- Check simulated database status.
- Identify stopped or unhealthy services.

Illustrative result:

```
{
  "ok": true,
  "services": {
    "nginx": "running",
    "tomcat": "running",
    "database": "running"
  }
}
```

The actual result schema should remain consistent with the implementation in `tools.py`.

### Tool 4 — Log Analyzer

**Function:** `analyze_logs()`

Purpose:

- Inspect simulated log entries.
- Identify errors related to resources or services.
- Provide additional diagnostic information when an earlier check detects a problem.

Example:

```
{
  "ok": true,
  "category": "resource",
  "level": "WARNING",
  "message": "Disk utilization reached 92%; temporary files may require cleanup."
}
```

Log analysis should run when the investigation identifies a reason to perform it, rather than being executed unconditionally in every workflow.

### Tool 5 — Tool Dispatcher

**Function:** `dispatch_tool()`

Purpose:

- Match a requested tool name to a registered function.
- Validate the requested tool and its arguments.
- Execute the corresponding function.
- Return structured results.
- Reject unknown tools safely.

Example invalid-tool result:

```
{
  "ok": false,
  "error": "Unknown tool: delete_server"
}
```

The dispatcher should allow only registered diagnostic tools. It must not execute arbitrary Python expressions or commands supplied by the language model.

### Utility — JSON Serialization

**Function:** `to_json()`

Purpose:

- Convert supported results into readable JSON.
- Display tool results in the terminal.
- Make debugging and report inspection easier.

Serialization should not be confused with tool execution. The dispatcher executes functions; serialization formats their results.

---

## 5\. Agent Workflow

The expected investigation follows this general process:

1. Receive the user's request.
2. Identify the diagnostic goal.
3. Select an appropriate tool.
4. Validate the tool name and arguments.
5. Execute the tool through the dispatcher.
6. Record the result.
7. Evaluate the result for problems.
8. Decide whether another tool is necessary.
9. Inspect logs when justified.
10. Combine the findings into a final report.
11. Return the report to the user.

### Example Workflow

User request:

> Investigate the server and tell me whether it is healthy.

The agent may perform the following investigation:

**Step 1: Server health check**

Determine whether the simulated server is available.

**Step 2: Resource monitoring**

Check CPU, memory, and disk utilization.

**Step 3: Service checks**

Inspect the simulated Nginx, Tomcat, and database services.

**Step 4: Conditional log analysis**

If disk utilization is above the configured threshold or a service is unhealthy, inspect relevant logs.

**Step 5: Consolidation**

Combine all available results into one report.

**Step 6: Final assessment**

Explain the findings, identify warnings, and suggest appropriate next steps.

The readings and workflow results are illustrative. The actual behavior depends on the configured simulated data.

---

## 6\. Step-by-Step Implementation

### Step 1 — Open the Day-23 Project

1. Open VS Code.
2. Open the existing `AI-Series/Practice-Lab` workspace.
3. Expand the `Day-23` directory.
4. Confirm that `app.py`, `models.py`, `requirements.txt`, `test_tools.py`, and `tools.py` are present.
5. Open each file and inspect the existing implementation before making changes.

**Why this step is required**

The project already contains work from the current Day-23 session. Inspecting it prevents accidental duplication and helps identify which functions are already implemented.

**Expected outcome**

The Day-23 files and their current responsibilities are understood.

### Step 2 — Activate the Virtual Environment

Open the integrated terminal and navigate to the Day-23 directory.

If the existing virtual environment is located one directory above Day-23, activate it from the project root.

For Git Bash:

```
source venv/Scripts/activate
```

For Windows PowerShell:

```
.\venv\Scripts\Activate.ps1
```

If the environment is located elsewhere, adjust the activation path accordingly.

Confirm that the terminal prompt displays the virtual environment name.

**Why this step is required**

The virtual environment isolates project dependencies from the system Python installation.

**Expected outcome**

The project uses the intended Python environment.

### Step 3 — Inspect and Validate the Existing Tools

Open `tools.py` and verify that the following functions exist:

- `check_server_health()`
- `monitor_resources()`
- `check_services()`
- `analyze_logs()`
- `dispatch_tool()`
- `to_json()`

Inspect their function signatures and return values.

Confirm:

- Tool names are registered consistently.
- Results use predictable data structures.
- Invalid tool names are rejected.
- Invalid arguments are handled safely.
- Log categories are validated.
- Tool execution does not require access to real servers.

Run the existing tests:

```
python test_tools.py
```

**Why this step is required**

The orchestration layer depends on the tools' actual interfaces. If a function expects a different argument format, the application must respect that contract.

**Expected outcome**

The existing diagnostic tools work independently before they are coordinated by the agent.

### Step 4 — Implement the Initial Orchestration Layer

Open `app.py`.

Create a function that executes a tool through `dispatch_tool()`, collects its result, and handles failures.

The wrapper should:

1. Accept a registered tool name.
2. Accept validated arguments.
3. Call the dispatcher.
4. Normalize the result when appropriate.
5. Preserve existing structured errors.
6. Convert unexpected execution failures into structured error results.

Do not let the language model execute tools directly. All execution should pass through the Python dispatcher.

**Why this step is required**

A shared execution wrapper gives the agent a consistent way to run different tools and record failures.

**Expected outcome**

The application can execute registered tools through one controlled interface.

### Step 5 — Implement Conditional Investigation

Add orchestration logic that evaluates resource and service results.

For example, configure a disk warning threshold:

```
DISK_WARNING_THRESHOLD = 85
```

If the simulated disk utilization is 92%, the agent should treat it as a warning and consider investigating the logs.

The threshold is a configurable example. It is not a universal operational limit.

Use explicit result fields when available. For example:

- Compare `disk_percent` against the configured threshold.
- Check service status fields for values such as `stopped` or `unhealthy`.
- Inspect structured health indicators.
- Handle missing or malformed results without assuming that the server is healthy.

When a problem is detected, invoke the log analyzer with a valid category supported by `tools.py`.

**Why this step is required**

Conditional execution is the central distinction between a basic tool-calling script and an orchestrated investigation. The result of one tool should influence what happens next.

**Expected outcome**

The agent can investigate problems selectively instead of executing every diagnostic tool unnecessarily.

### Step 6 — Combine Tool Results

Create a report structure that records the tool name and its result.

For example:

```
{
  "investigation": "server_health",
  "steps": [
    {
      "tool": "check_server_health",
      "result": {}
    },
    {
      "tool": "monitor_resources",
      "result": {}
    },
    {
      "tool": "check_services",
      "result": {}
    }
  ]
}
```

The empty objects above are placeholders. During execution, populate them with the actual tool results.

Include log analysis only if it was executed.

The report should distinguish between:

- A successful check.
- A detected warning.
- A failed check.
- A tool execution error.
- A check that was skipped.

A failed check must not be interpreted as proof that the server is healthy.

**Why this step is required**

A consolidated report lets the user understand the investigation without manually combining separate terminal outputs.

**Expected outcome**

All executed diagnostic steps and their results are available in a single structured report.

### Step 7 — Implement the Model Integration

Open `models.py` and inspect its current implementation.

Configure the application to communicate with the local Ollama service and the installed Llama 3.2 model.

Before integrating the model, verify that Ollama is installed and that the required model is available.

For example, from the terminal:

```
ollama --version
ollama list
```

If the model is not available, obtain it through Ollama:

```
ollama pull llama3.2
```

Then verify that the model can respond to a simple prompt using the interface supported by your installed Ollama version.

Keep model configuration and model communication in `models.py`, rather than mixing them into the diagnostic functions.

**Why this step is required**

The local model will interpret the user's request and help determine which registered tool should run next.

**Expected outcome**

The Python application can communicate with the configured local model.

### Step 8 — Give the Model a Tool Registry

Define a clear description for every registered tool.

Each description should specify:

- Tool name.
- Purpose.
- Accepted arguments.
- Argument types.
- Expected result structure.
- Conditions under which the tool is useful.

For example:

```
{
  "name": "monitor_resources",
  "description": "Check simulated CPU, memory, and disk utilization.",
  "parameters": {
    "type": "object",
    "properties": {},
    "additionalProperties": false
  }
}
```

This example describes a tool without arguments. Match the actual schema to the implemented function.

The model should select from the registered tools instead of inventing arbitrary function names.

**Why this step is required**

A tool registry establishes the contract between the model and the Python execution layer.

**Expected outcome**

The model has clear information about the tools it is allowed to request.

### Step 9 — Implement the Tool-Calling Loop

The application should support a controlled interaction between the model and Python.

A typical cycle is:

1. Send the user's request and available tool descriptions to the model.
2. Receive the model's response.
3. Determine whether the response requests a tool call.
4. Validate the requested tool name.
5. Validate its arguments.
6. Execute the tool through `dispatch_tool()`.
7. Return the result to the model in the format expected by the integration.
8. Allow the model to interpret the result and choose the next action.
9. Continue until the model provides a final answer or a safety limit is reached.

The exact request and response format depends on the Ollama API and the integration supported by the installed version.

Do not assume that every Llama 3.2 response is a valid tool call. Parse the actual structured response and handle malformed or unsupported requests.

**Why this step is required**

This is where the model begins to select tools dynamically instead of relying exclusively on a fixed Python sequence.

**Expected outcome**

The model can request registered tools, receive their results, and continue the investigation based on the evidence.

### Step 10 — Add Execution Limits

Configure limits for:

- Maximum model/tool interaction rounds.
- Maximum tool calls per investigation.
- Valid registered tool names.
- Valid argument structures.
- Maximum acceptable output size.
- Tool execution failures.

For example:

```
MAX_AGENT_ROUNDS = 8
```

This is an illustrative starting limit, not a requirement for every investigation.

If the limit is reached, stop safely and report that the investigation could not be completed within the configured limit.

**Why this step is required**

An agent may repeatedly request the same tool or fail to reach a conclusion. Execution limits prevent unbounded loops and unnecessary resource consumption.

**Expected outcome**

The agent operates within a defined execution budget and exits safely when it cannot make further progress.

### Step 11 — Improve Failure Handling

Test the following situations:

- Unknown tool name.
- Invalid log category.
- Malformed tool arguments.
- Tool function raises an exception.
- Tool returns malformed data.
- Ollama is unavailable.
- The model returns an invalid tool request.
- The model repeatedly requests the same tool.
- A diagnostic result is missing.
- A diagnostic check fails.

The application should record the error, preserve previously collected evidence, and explain any resulting uncertainty.

Do not report a healthy server merely because a diagnostic function failed.

**Why this step is required**

Reliable failure handling is necessary for a DevOps agent because incomplete evidence must not be presented as a confirmed healthy state.

**Expected outcome**

The application produces controlled errors and useful diagnostic reports rather than crashing or inventing successful results.

### Step 12 — Test the Full Investigation

Run the existing tool tests:

```
python test_tools.py
```

Then run the application:

```
python app.py
```

Test a request such as:

```
Investigate the server and tell me whether it is healthy.
```

Confirm that:

1. The user request is received.
2. The model or orchestration logic selects appropriate tools.
3. Tool arguments are validated.
4. The tools return structured results.
5. Conditional investigation occurs when required.
6. The final report combines the collected evidence.
7. Invalid tool calls are rejected.
8. Execution limits work.
9. The program exits without an unhandled exception.

Add dedicated tests for `app.py` to verify the conditional branches and the tool-calling loop. Passing `test_tools.py` alone does not prove that the entire agent works correctly.

**Why this step is required**

The complete workflow must be validated, not just its individual Python functions.

**Expected outcome**

The Day-23 agent can complete a simulated server investigation and produce a consolidated report.

---

## 7\. Recommended Testing Scenarios

| Scenario | Expected behavior |
| --- | --- |
| All simulated checks are healthy | Report the findings and avoid unnecessary log inspection |
| Disk usage exceeds the configured threshold | Flag a resource warning and investigate relevant logs |
| Nginx or Tomcat is stopped | Identify the service problem and investigate relevant logs |
| Database status is unhealthy | Report the service problem |
| A tool name is invalid | Reject the request safely |
| Arguments are malformed | Reject or report the invalid arguments |
| A tool raises an exception | Record the failure and preserve other findings |
| Ollama is unavailable | Report that model-driven execution could not continue |
| The model returns an invalid tool request | Reject it without executing arbitrary code |
| The model exceeds the execution limit | Stop safely and report incomplete investigation |

---

## 8\. Important Design Principles

### Separation of Responsibilities

Keep the model, dispatcher, and diagnostic functions separate.

- `models.py` handles model communication.
- `tools.py` contains the simulated diagnostic functions and their execution interfaces.
- `app.py` coordinates the investigation.
- `test_tools.py` verifies tool behavior.

### Validate Every Tool Call

Treat the model's output as untrusted input. Validate tool names, argument types, required fields, and permitted values before execution.

### Prefer Structured Data

Use explicit fields and numeric thresholds rather than relying on keyword searches through serialized JSON.

### Preserve Evidence

Keep the results of successful checks even when another tool fails. Clearly identify missing or unreliable evidence.

### Keep Server Operations Simulated

Do not execute real system commands, modify services, delete files, or make configuration changes in this project.

### Avoid Unnecessary Tool Calls

Use conditional execution to investigate relevant problems without running every tool repeatedly.

### Separate Model Reasoning from Execution

The model can propose the next tool call, but Python remains responsible for validation, execution, limits, and error handling.

---

## 9\. Common Mistakes and Corrections

### Mistake 1 — Assuming successful tool tests mean the agent is complete

**Correction:** Tool tests validate individual functions. The complete application needs separate tests for orchestration, conditional execution, model integration, and failure handling.

### Mistake 2 — Running log analysis after every check

**Correction:** Inspect logs when earlier findings justify further investigation. An unconditional call defeats the purpose of conditional orchestration.

### Mistake 3 — Treating every warning keyword as proof of a problem

**Correction:** Use structured status fields and numeric thresholds. Text matching can produce false positives.

### Mistake 4 — Allowing the model to execute arbitrary function names

**Correction:** Only registered tools may be executed, and every request must be validated before dispatch.

### Mistake 5 — Treating a failed check as a healthy result

**Correction:** Represent tool failures and incomplete investigations explicitly.

### Mistake 6 — Mixing tool functions with model communication

**Correction:** Keep the diagnostic functions in `tools.py` and model integration in `models.py`. Use `app.py` to coordinate them.

### Mistake 7 — Assuming example readings are actual server measurements

**Correction:** All readings in this project are simulated and must be presented as such.

### Mistake 8 — Building model integration before validating the dispatcher

**Correction:** First verify the Python tools and orchestration interfaces. Then connect the model to a stable execution contract.

---

## 10\. Definition of Done

Day 23 is complete when all of the following conditions are satisfied:

- [ ]The diagnostic tools work independently.
- [ ]The dispatcher recognizes only registered tools.
- [ ]Tool arguments are validated.
- [ ]The application coordinates multiple tools.
- [ ]Results from one check can influence subsequent actions.
- [ ]Log analysis runs conditionally when justified.
- [ ]Results are combined into a consolidated report.
- [ ]Model integration uses the configured Ollama model.
- [ ]The model can request registered tools through a controlled interface.
- [ ]Tool and model failures are handled safely.
- [ ]Execution limits prevent unbounded tool-calling loops.
- [ ]Tests cover the important orchestration scenarios.
- [ ]All server readings remain simulated.
- [ ]The application runs successfully from the command line.

---

## 11\. Final Expected Outcome

At the end of Day 23, the project should demonstrate a Multi-Tool AI DevOps Agent capable of:

1. Understanding a server-investigation request.
2. Selecting appropriate diagnostic tools.
3. Executing tools through a controlled Python dispatcher.
4. Evaluating diagnostic results.
5. Performing conditional log investigation.
6. Combining evidence into a readable report.
7. Handling invalid requests and execution failures.
8. Using a local LLM without allowing it to bypass execution controls.

---
### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/2d6ad0ed-7e6e-4839-8cb1-a3092edbae94" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/f7c6fb7b-8448-463f-8e39-b8912dc28e1b" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/1a58733b-7e25-4d75-be17-224e2aeb97f3" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/9b95e051-9d69-4e46-8138-c3468a85b145" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/4e6a8216-11ca-41c0-92dc-3d52c1572cd4" />





