# Day-1
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

# Day-2

# OpenAI API Chatbot — Notes

## 1. Objective

The goal is to build a simple AI role-play chatbot using OpenAI's API.

In this task, the chatbot acts as a **friendly travel guide**. It should greet the user and ask where they want to go.

The Python program will:

1. Configure the OpenAI API client.
2. Read the API credentials from environment variables.
3. Define a prompt.
4. Send the prompt to an OpenAI chat model.
5. Store the API response in `nameresponse`.
6. Extract the generated text.
7. Print the generated response.

---

## 2. Working Directory

All work should be performed inside:

```text
/root/openaiproject
```

Move into this directory before creating or running the project:

```bash
cd /root/openaiproject
```

Keeping the project files in the required directory is important because the task specifically expects the chatbot project there.

---

## 3. Python Virtual Environment

A virtual environment keeps the project's Python packages isolated from the system Python installation.

Create the virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

After activation, installing packages affects this project environment rather than the global Python installation.

---

## 4. Installing the OpenAI Package

The Python program needs the OpenAI SDK.

Install it inside the activated virtual environment:

```bash
pip install openai
```

The important sequence is:

```bash
python3 -m venv venv
source venv/bin/activate
pip install openai
```

The OpenAI package provides the `OpenAI` client used by the Python program.

---

## 5. API Credentials

The API credentials are available through `/root/.bash_profile`.

The expected environment variables are:

```text
OPENAI_API_KEY
OPENAI_API_BASE
```

Load the profile before running the program:

```bash
source /root/.bash_profile
```

The program can then read the values using Python's `os.environ.get()`.

This avoids hardcoding the credentials directly into the source code.

---

## 6. Importing Required Modules

The chatbot needs two things:

```python
import os
from openai import OpenAI
```

### `os`

The `os` module allows Python to access environment variables.

### `OpenAI`

`OpenAI` is the client class supplied by the OpenAI Python package.

---

## 7. Reading the API Configuration

The credentials are read from environment variables:

```python
api_key = os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("OPENAI_API_BASE")
```

Here:

- `OPENAI_API_KEY` contains the API key.
- `OPENAI_API_BASE` contains the API base URL.
- `os.environ.get()` retrieves their values.

---

## 8. Creating the OpenAI Client

Create the client using the API key and base URL:

```python
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)
```

The `client` object is then used to communicate with the OpenAI API.

The `base_url` is included because this task specifies that the API base should be configurable through `OPENAI_API_BASE`.

---

## 9. Defining the Prompt

The required prompt is:

```python
prompt = "You are a friendly travel guide. Greet the user and ask where they want to go."
```

A **prompt** is the instruction given to the AI model.

In this case, the instruction tells the model to behave as a travel guide and produce a greeting followed by a question about the user's destination.

The exact wording is important because it is part of the task requirements.

---

## 10. Sending the Prompt to the Chat Model

The chat completion request is made with:

```python
nameresponse = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=100
)
```

The result is stored in:

```python
nameresponse
```

This variable name is required by the task.

---

## 11. Model

The requested model is:

```text
openai/gpt-4.1-mini
```

It is specified with:

```python
model="openai/gpt-4.1-mini"
```

The model determines which AI system processes the prompt.

---

## 12. Messages

The request contains:

```python
messages=[
    {"role": "user", "content": prompt}
]
```

A chat request uses messages to provide conversational input to the model.

The message has two important fields:

- `role` — identifies who is sending the message.
- `content` — contains the actual instruction.

Here the role is:

```text
user
```

and the content is the value stored in `prompt`.

---

## 13. Temperature

The task requires:

```python
temperature=0.7
```

Temperature controls how much variation is allowed in the model's output.

A higher temperature generally allows more variation, while a lower temperature generally produces more consistent output.

For this task, the exact required value is `0.7`.

---

## 14. Maximum Tokens

The task requires:

```python
max_tokens=100
```

This limits the amount of generated output.

Since the chatbot only needs a short greeting and question, 100 tokens is sufficient for the requested response.

---

## 15. Extracting the Generated Text

The API response contains more information than just the generated sentence.

The generated assistant text can be extracted with:

```python
nameresponse.choices[0].message.content
```

The program prints it using:

```python
print(nameresponse.choices[0].message.content)
```

The important idea is:

```text
nameresponse
    ↓
choices
    ↓
first choice [0]
    ↓
message
    ↓
content
    ↓
generated text
```

---

## 16. Complete Program

The complete `chatbot.py` file is:

```python
import os
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY")
base_url = os.environ.get("OPENAI_API_BASE")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

prompt = "You are a friendly travel guide. Greet the user and ask where they want to go."

nameresponse = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=100
)

print(nameresponse.choices[0].message.content)
```

---

## 17. Running the Program

From `/root/openaiproject`, activate the environment and load the environment variables:

```bash
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
```

Then run:

```bash
python chatbot.py
```

The program sends the prompt to the model and prints the generated response.

---

## 18. Expected Output

The exact wording can vary because the response is generated by the AI.

A response could look similar to:

```text
Hello, traveler! I'm your friendly travel guide. Where would you like to go?
```

The important requirement is that the response should greet the user and ask where they want to go.

---

## 19. Important Points to Remember

- Work inside `/root/openaiproject`.
- Create and activate a virtual environment before installing OpenAI.
- Install the `openai` package inside the virtual environment.
- Load `/root/.bash_profile` so the API environment variables are available.
- Use `OPENAI_API_KEY` and `OPENAI_API_BASE`.
- Create the `OpenAI` client with `api_key` and `base_url`.
- Use model `openai/gpt-4.1-mini`.
- Store the required prompt in `prompt`.
- Store the API response in `nameresponse`.
- Use `temperature=0.7`.
- Use `max_tokens=100`.
- Print `nameresponse.choices[0].message.content`.
- API requests should be used judiciously because the task specifies a maximum of 10 requests.

---

## 20. Overall Flow

The complete workflow can be remembered as:

```text
Project directory
       ↓
Create virtual environment
       ↓
Activate virtual environment
       ↓
Install openai
       ↓
Load API environment variables
       ↓
Import OpenAI
       ↓
Create client
       ↓
Define prompt
       ↓
Call chat model
       ↓
Store response in nameresponse
       ↓
Extract message content
       ↓
Print AI response
```

This demonstrates the basic pattern for connecting a Python application to an OpenAI-compatible chat API and displaying the model's generated response.
