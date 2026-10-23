# 🚀 Day 32 — Build a Local AI Evaluation & Testing Framework 🧪🤖

## Objective

Build a local AI evaluation framework using Python, Ollama, Streamlit, Pandas, and Pytest. The application tests AI responses, scores their quality, compares prompts, identifies failures, and exports evaluation reports.

## Tech Stack

- Python
- Ollama — `qwen3:4b`
- Streamlit
- Pandas
- Requests
- Pytest
- JSON / CSV

## Project Structure

```
Day-32/
├── .venv/
├── app.py
├── test_cases.json
├── test_scoring.py
└── requirements.txt
```

## Step 1 — Environment Setup

Create the project and virtual environment:

```
cd D:\AI-Series\Practice-Lab
mkdir Day-32
cd Day-32
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```
python -m pip install --upgrade pip
pip install streamlit pandas requests pytest
```

Verify Ollama and the model:

```
ollama --version
ollama list
ollama pull qwen3:4b
```

## Step 2 — requirements.txt

```
streamlit
pandas
requests
pytest
```

## Step 3 — test\_cases.json

Stores questions, expected answers, required keywords, reference context, and expected output format.

```
[
  {
    "id": "T01",
    "question": "What is Python?",
    "expected_answer": "Python is a high-level programming language used for scripting, automation, web development, and data analysis.",
    "must_include": ["programming language", "automation"],
    "context": "",
    "expected_format": "paragraph"
  },
  {
    "id": "T02",
    "question": "Write a Python function that adds two numbers.",
    "expected_answer": "Define a function that accepts two numbers and returns their sum.",
    "must_include": ["def", "return"],
    "context": "",
    "expected_format": "code"
  },
  {
    "id": "T03",
    "question": "According to the supplied context, how many days does the trial last?",
    "expected_answer": "The trial lasts 14 days.",
    "must_include": ["14 days"],
    "context": "The software trial lasts 14 days. A payment method is required after the trial ends.",
    "expected_format": "paragraph"
  }
]
```

## Step 4 — app.py

The application connects to Ollama's local API, generates answers, evaluates responses, compares prompts, displays results in Streamlit, and exports reports.

The evaluation metrics are:

- **Relevance:** Keyword overlap between the question and answer.
- **Completeness:** Coverage of required keywords.
- **Clarity:** Basic response length and sentence-count checks.
- **Instruction following:** Checks whether the expected output format is followed.
- **Groundedness:** Lexical overlap with supplied reference context.
- **Overall score:** Average of the available metric scores.
- **Pass/fail:** Based on the overall score and minimum completeness and instruction-following thresholds.

The app includes three tabs: Run Evaluation, Compare Prompts, and Results. It displays scores, a progress bar, failed tests, and downloadable JSON and CSV reports.

Ollama generates each answer locally. The current implementation waits for each answer to finish before updating the next test's progress.

## Step 5 — test\_scoring.py

Contains three automated tests:

1. Checks that required keywords receive a completeness score of 100.
2. Checks that missing required keywords reduce completeness.
3. Checks that groundedness is calculated when reference context is available.

Run the tests:

```
python -m pytest -v test_scoring.py
```

Expected result: **3 tests passed**.

## Step 6 — Run the Application

Start the dashboard:

```
python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually:

```
http://localhost:8501
```

Keep the terminal open while using the application.

## Step 7 — Evaluate AI Responses

1. Select the installed Ollama model, such as `qwen3:4b`.
2. Enter or retain the system prompt.
3. Click **Run all tests**.
4. Inspect generated answers, scores, and pass/fail results.
5. Download the evaluation report in JSON or CSV format.

## Step 8 — Compare Prompts

1. Open the Compare Prompts tab.
2. Enter Prompt A and Prompt B.
3. Click Compare Prompts.
4. Review the scores and comparison chart.
5. Download the comparison CSV.

Both prompts use the same test cases and model, making their results easier to compare.

## Step 9 — Test Failure Tracking

Temporarily add `"quantum computing"` to the required keywords for test T01 in `test_cases.json`.

Run the evaluation again and inspect the completeness score. Restore the original keywords afterward.

This demonstrates how evaluation criteria can identify potential failures. Poorly designed criteria can also penalize correct answers, so test cases must be reviewed carefully.

## Limitations

The current scoring system uses simple heuristics rather than semantic understanding. Keyword overlap does not prove factual correctness or groundedness. The application retains results in Streamlit session state, so they should be downloaded for permanent storage.

## Final Outcome

Day 32 introduces repeatable AI testing, local model evaluation, transparent quality scoring, prompt comparison, failure tracking, automated scoring tests, and report export. These are foundational skills for LLM evaluation, regression testing, prompt optimization, and LLMOps.

### Screenshots
