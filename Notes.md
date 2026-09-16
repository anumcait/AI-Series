# Notes — AI Bug Description Clarifier

## 1. Goal

The task is to build a small Python program that takes an informal bug report and uses an OpenAI model to rewrite it into a clear, structured, professional bug summary.

### Example input

```text
App keeps crashing when I click save.
```

The AI should turn this into something clearer, such as:

```text
Bug Summary:
Application crashes upon clicking the "Save" button.

Triggering Action:
User clicks the "Save" button.

Observed Behavior:
The application unexpectedly crashes immediately after the button is clicked.
```

---

## 2. Project Location

The required project directory is:

```text
/root/openaiproject
```

Always work inside this directory for this task.

```bash
cd /root/openaiproject
```

---

## 3. Virtual Environment

A virtual environment keeps the project's Python packages separate from the system Python installation.

Create and activate it with:

```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, the terminal normally shows `(venv)` at the beginning of the prompt.

Install the OpenAI Python package:

```bash
pip install openai
```

The important package is `openai`, because the Python program uses the OpenAI client.

---

## 4. OpenAI Credentials

The API credentials are already available through environment variables.

The program reads them with:

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

This is preferable to putting secret credentials directly into the source code.

---

## 5. Initialize the OpenAI Client

Import the required modules:

```python
import os
from openai import OpenAI
```

Then initialize the client:

```python
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)
```

Here:

- `OPENAI_API_KEY` provides authentication.
- `OPENAI_API_BASE` specifies the API endpoint.
- `OpenAI(...)` creates the client used to communicate with the API.

---

## 6. The `clarify_bug()` Function

The task requires a function with this signature:

```python
def clarify_bug(description: str) -> str:
```

The function receives the developer's raw bug description and returns the AI-generated clarification.

The input must be used dynamically. Do not permanently put the bug description inside the prompt.

For example:

```python
prompt = f"""
Rewrite the following informal bug report into a clear, structured,
professional bug summary suitable for a developer issue tracker.
Include the problem, triggering action, and observed behavior.
Do not invent details.

Raw bug report:
{description}
"""
```

The `f` before the string allows the value of `description` to be inserted into the prompt.

---

## 7. Calling the Chat Completion API

The task specifies these exact settings:

- Model: `openai/gpt-4.1-mini`
- Message role: `user`
- `max_tokens`: `100`
- `temperature`: `0.0`

The API call is:

```python
response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=100,
    temperature=0.0,
)
```

### Why `temperature=0.0`?

A temperature of `0.0` makes the model's output more consistent and deterministic, which is useful when transforming bug reports into predictable summaries.

### Why `max_tokens=100`?

The task specifically limits the generated response to 100 tokens, keeping the clarification concise.

---

## 8. Getting the AI's Text

The generated text is available through:

```python
response.choices[0].message.content
```

The function returns it:

```python
return response.choices[0].message.content
```

The variable `response` is also required by the task, so the API result should be stored in that variable.

---

## 9. Running the Required Input

The specified bug report is:

```python
description = "App keeps crashing when I click save."
```

Then call the function:

```python
response = clarify_bug(description)
```

Finally print the result:

```python
print(response)
```

This displays the AI-generated clarification in the terminal.

---

## 10. Complete Program

The complete `bug_clarifier.py` should look like this:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)

def clarify_bug(description: str) -> str:
    prompt = f"""
Rewrite the following informal bug report into a clear, structured,
professional bug summary suitable for a developer issue tracker.
Include the problem, triggering action, and observed behavior.
Do not invent details.

Raw bug report:
{description}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.0,
    )

    return response.choices[0].message.content

description = "App keeps crashing when I click save."
response = clarify_bug(description)
print(response)
```

---

## 11. Execution

From `/root/openaiproject`:

```bash
source venv/bin/activate
python bug_clarifier.py
```

A successful execution produces a professional bug summary, for example:

```text
Bug Summary:
Application crashes upon clicking the "Save" button.

Triggering Action:
User clicks the "Save" button within the application.

Observed Behavior:
The application unexpectedly crashes immediately after the "Save" button is clicked.
```

The exact wording can vary because the response is generated by the AI.

---

## 12. Important Task Requirements

Before considering the task complete, check that:

- The file is `/root/openaiproject/bug_clarifier.py`.
- A Python virtual environment is created.
- The `openai` package is installed.
- The OpenAI client uses the environment credentials.
- `clarify_bug(description: str) -> str` exists.
- The developer's input is inserted dynamically into the prompt.
- The model is `openai/gpt-4.1-mini`.
- The message role is `user`.
- `max_tokens=100`.
- `temperature=0.0`.
- The API result is stored in `response`.
- The clarified result is printed.
- The specified input is `"App keeps crashing when I click save."`.

---

## 13. API Request Limit

The task allows a maximum of **10 API requests** before rate limiting.

Therefore, once the script successfully produces the expected output, do not repeatedly execute it unnecessarily.

For a KodeKloud task, after successful execution, proceed to the task's **Check** button.

---

## 14. Key Concepts Learned

### Environment variables

Used to safely obtain configuration and credentials:

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

### Type hints

The function declaration:

```python
def clarify_bug(description: str) -> str:
```

means:

- `description` is expected to be a string.
- The function returns a string.

### Dynamic prompts

The raw developer report is inserted into the prompt using:

```python
{description}
```

inside an f-string.

### API response

The generated assistant text is extracted with:

```python
response.choices[0].message.content
```

### Virtual environments

A virtual environment isolates project dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

This prevents the project's packages from interfering with the system Python installation.

---

## 15. Overall Flow

```text
Developer's informal bug report
            ↓
       clarify_bug()
            ↓
   Construct dynamic prompt
            ↓
   OpenAI Chat Completion API
            ↓
     AI clarifies the bug
            ↓
 Extract response text
            ↓
       Print summary
```

The core idea is simple: **take an unclear human-written bug report, provide it to the AI with clear transformation instructions, and return a concise professional issue description.**
