# 🚀 Day 36 — Build a Local AI Rate Limiting & Circuit Breaker System ⚡🛡️

## Objective

Build a local AI application using Python, Streamlit, Ollama, Qwen3, SQLite, Pandas, and Plotly to control request traffic, handle model failures, and monitor system activity.

## 1\. Project Setup

- Open the `Day-36` folder in VS Code.
- Create and activate a Python virtual environment.
- Install dependencies:bash
  ```
  pip install streamlit requests pandas plotly
  ```
- Install Ollama and verify that the local service is running.
- Check installed models using `ollama list`.

## 2\. Model Configuration

The installed models were verified using Ollama. The model used for this project is:

python

```
MODEL = "qwen3:4b"
```

The initial `qwen3:1.7b` configuration failed because that model was not installed.

## 3\. Application Implementation

Created `app.py` containing:

- Streamlit user interface for entering a user ID and AI prompt.
- Per-user rate limiter allowing 5 requests per rolling 60-second window.
- Circuit breaker with `CLOSED`, `OPEN`, and `HALF_OPEN` states.
- Failure threshold of 3 failed requests.
- Recovery interval of 30 seconds.
- Request timeout and one retry for failed requests.
- Fallback message when the AI service is unavailable.
- SQLite request history stored in `requests.db`.
- Dashboard metrics, Plotly chart, and recent request history.

## 4\. Run the Application

Start the application from the `Day-36` directory:

bash

```
python -m streamlit run app.py
```

Open the local address:

text

```
http://localhost:8501
```

The dashboard displays the model configuration, rate limit, failure threshold, recovery interval, request counters, circuit state, and request history.

## 5\. Troubleshooting Completed

- Identified that `qwen3:1.7b` was not installed.
- Verified the installed model `qwen3:4b` using `ollama list`.
- Investigated initial HTTP 404 errors and subsequent request timeouts.
- Tested the Ollama generation endpoint directly using `curl`.
- Confirmed that Qwen3 can return a successful response containing `"response": "Hello"`.
- Observed that model generation time varies with the requested output and available computing resources.
- Identified Streamlit and Plotly deprecation warnings as separate from the model request errors.

For further testing, configure the generation request with `think=False` and a bounded output token count, where supported by the installed Ollama version and model. Adjust the timeout according to measured response times.

## 6\. Practical Tests to Complete

1. Submit a prompt and verify that an AI answer is displayed.
2. Send five requests using the same user ID within 60 seconds; verify that the sixth is blocked.
3. Temporarily use an unavailable local API port and trigger three failed requests.
4. Verify that the circuit opens and blocks further model calls.
5. Restore the correct Ollama endpoint and test recovery after 30 seconds.
6. Verify that request outcomes appear in the SQLite history and dashboard.

## 7\. Project Files

- `app.py` — Application and dashboard.
- `requests.db` — Persistent request history, created automatically.
- `.venv/` — Python virtual environment.
- `day.md` — Project notes and documentation.

## Key Learning

Rate limiting protects the application from excessive requests. Circuit breakers prevent repeated calls to an unhealthy service, while timeouts, controlled retries, fallback messages, and persistent monitoring improve reliability.

**Status:** Streamlit and the local Ollama API have been tested. Qwen3 generation has returned a successful response directly through the API. Complete the end-to-end dashboard, rate-limit, circuit-breaker, and recovery tests to verify the full Day 36 project.