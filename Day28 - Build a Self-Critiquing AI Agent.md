# 🚀 Day 28 — Build a Self-Critiquing AI Agent 🧠🔍

## Objective

Build a local AI agent using Python, Ollama, and Llama 3.2 that generates an answer, evaluates its quality against defined criteria, improves weak answers, and saves the evaluation results to a JSON file.

The key lesson is:

**Generating an answer is not enough. An AI agent should evaluate and improve its output before delivering it.**

The model performs the generation and self-critique, while Python controls the evaluation workflow, validates scores, and limits improvement attempts.

## 1\. Technology Stack

- Python
- Ollama
- Llama 3.2
- JSON
- Requests library
- Prompt engineering
- AI evaluation and iterative refinement

## 2\. Project Structure

Create the following project:

```
day28-self-critique/
├── agent.py
├── evaluations.json
└── .venv/
```

File descriptions:

- `agent.py` — contains answer generation, evaluation, improvement, retry control, and report saving.
- `evaluations.json` — stores the initial and final answers, evaluation scores, and attempt history. It is created automatically.
- `.venv/` — contains the project's isolated Python environment.

## 3\. Install and Configure the Environment

### Step 1: Check Python

Run:

```
python --version
```

Expected result: Python displays its installed version. Use Python 3.10 or newer.

### Step 2: Check Ollama

Run:

```
ollama --version
```

Expected result: Ollama displays its version.

### Step 3: Download Llama 3.2

Run:

```
ollama pull llama3.2
```

Expected result: The model downloads and becomes available locally.

### Step 4: Test the Model

Run:

```
ollama run llama3.2
```

Type:

```
Explain AI agents in two sentences.
```

Confirm that the model responds, then exit using:

```
/bye
```

### Step 5: Create a Virtual Environment

Run:

```
python -m venv .venv
```

Activate it on Windows PowerShell:

```
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```
source .venv/bin/activate
```

### Step 6: Install Dependencies

Run:

```
pip install requests
```

Expected result: The Requests library is installed and Python can communicate with Ollama's local API.

## 4\. Define the Agent Workflow

The agent follows this sequence:

1. The user enters a task.
2. Ollama generates an initial answer.
3. The evaluator scores the answer against four criteria.
4. The evaluator identifies strengths, weaknesses, and improvements.
5. Python calculates the total score.
6. If the score is below 16/20, the agent requests an improved answer.
7. The revised answer is evaluated again.
8. The process stops when the score reaches the threshold or two improvement attempts have been used.
9. Python displays the initial and final answers and saves the report to `evaluations.json`.

The maximum number of improvement attempts must be enforced by Python, not by the LLM.

## 5\. Implement the AI Agent

Create `agent.py` and implement these functions:

### `ask_model(prompt, json_mode=False)`

Send a request to Ollama's chat API:

```
http://localhost:11434/api/chat
```

Use the `llama3.2` model and disable streaming so the complete response can be processed.

When evaluating an answer, request JSON output.

Expected result: The function returns the model's response as text.

### `evaluate(task, draft)`

Ask the model to evaluate the draft against four criteria:

- Relevance — does it answer the actual task?
- Completeness — does it cover the important details?
- Clarity — is it easy to understand?
- Format — does it follow the requested format?

Each criterion receives a score from 1 to 5.

The evaluation must also include strengths, weaknesses, and suggested improvements.

Example scorecard:

```
{
  "relevance": 5,
  "completeness": 3,
  "clarity": 4,
  "format": 5,
  "strengths": ["Answers the main question"],
  "weaknesses": ["Missing a practical example"],
  "improvements": ["Add a simple example"]
}
```

Validate that every score is an integer between 1 and 5 and that feedback fields are lists.

Expected result: A structured evaluation that Python can process.

### `improve(task, draft, report)`

Send the original task, current answer, and evaluation feedback to Ollama.

Ask the model to address the identified weaknesses while preserving correct information.

Expected result: An improved answer without the evaluation commentary.

### `run_agent(task)`

Implement the main workflow:

1. Generate the initial answer.
2. Store a copy for comparison.
3. Evaluate the current answer.
4. Calculate the total score out of 20.
5. Record each answer and its evaluation in the history.
6. Stop if the score reaches 16/20 or the retry limit is reached.
7. Otherwise, improve the answer and repeat the evaluation.
8. Display the initial and final answers and scorecards.
9. Save the complete report to `evaluations.json`.

Use these settings:

```
MODEL = "llama3.2"
MAX_RETRIES = 2
PASS_SCORE = 16
```

Expected result: A controlled self-critique loop that cannot improve indefinitely.

## 6\. Implement Evaluation Logging

Save each run to `evaluations.json`.

Each report should contain:

- Timestamp and model name
- Original task
- Initial answer
- Final answer
- Initial and final scorecards
- Initial and final total scores
- Number of improvement attempts
- Complete evaluation history

Append new reports to the existing JSON list instead of overwriting previous runs.

Expected result: Evaluation results remain available for comparison after the program exits.

## 7\. Run the Agent

Ensure Ollama is running, then execute:

```
python agent.py
```

Enter this task:

```
Explain the difference between embeddings and a vector database.
Include an example and use simple language.
```

Expected result:

- The agent generates an initial answer.
- The evaluator scores all four criteria.
- Weaknesses are identified.
- The answer is improved when the total score is below 16.
- The final answer and evaluation report are displayed.
- The report is saved to `evaluations.json`.

Actual scores and the number of retries depend on the model's responses.

## 8\. Test the Agent

### Test 1: Simple Task

Input:

```
Explain Python in two sentences.
```

Expected result: The agent generates and evaluates an answer. It may finish without improvement if the score reaches the threshold.

### Test 2: Detailed Task

Input:

```
Explain embeddings versus vector databases with an example and a comparison table.
```

Expected result: The evaluator checks completeness and formatting and requests improvements if the score is too low.

### Test 3: Retry Limit

Run a task with several specific requirements.

Expected result: The agent never uses more than two improvement attempts, even if the final score remains below 16/20.

### Test 4: Report Persistence

Run the agent twice and inspect `evaluations.json`.

Expected result: Both reports are preserved in the JSON list, including their evaluation histories.

## 9\. Troubleshooting

### Ollama Connection Error

Check that Ollama is installed and running.

Run:

```
ollama list
```

Expected result: `llama3.2` appears in the available models.

### Missing Requests Library

Run:

```
pip install requests
```

Ensure your virtual environment is activated.

### Invalid JSON Evaluation

The model may return malformed JSON or unexpected fields.

The program should report the error and stop rather than accept invalid scores.

### Slow Responses

Local inference depends on your hardware. Allow time for the model to generate and evaluate each answer.

### Final Score Remains Below 16

The retry limit may be reached before the answer meets the threshold. The program should still save the final result and report its actual score.

Do not treat a high model-generated score as proof of factual correctness.

## Key Learning

A self-critiquing AI agent introduces quality control into the generation process.

**Generate → Evaluate → Improve → Deliver**

You have implemented structured evaluation, feedback-driven refinement, retry limits, score comparison, and persistent JSON reporting.

The evaluator can still overlook factual errors because the same model generates and judges the answer. Independent verification is necessary for stronger reliability.

## Outcome

Built a local self-critiquing AI agent using Python, Ollama, and Llama 3.2 that evaluates its answers, improves them when necessary, and saves its results for later inspection.

This provides the foundation for Day 29: building an AI workflow agent that combines planning, tool calling, memory, evaluation, and controlled approval.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/55c9606a-a7d6-4920-a8b9-5706e260fb4c" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/a65f6769-0aa3-49c2-8838-b506675c2e1f" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/2067b68e-8e9c-45af-8512-773eabb83d10" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/356ec275-c227-49ef-b600-4d6921815060" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/09302bd4-df26-4a52-8fa3-a5ff06c4f0e9" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/6b97a983-454a-4618-91c5-cad5354c3571" />






