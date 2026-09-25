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

---

# Day 3 — AI Comment Generator

## 1. The Main Idea

One useful application of AI in software development is **automatically understanding and documenting code**.

When developers write code, they often need comments or docstrings to explain what the code does. For simple functions this is easy, but in large projects, manually documenting everything can take a lot of time.

AI can help by taking a piece of code as input and generating a short description of its purpose.

For example:

```python
def calculate_area(length, width):
    return length * width
```

An AI model can understand that the function multiplies `length` and `width` to calculate an area and produce a comment such as:

```text
# Calculates the area using the given length and width.
```

So the basic concept is:

**Source code → AI → Human-readable explanation**

---

## 2. What is an AI Module?

An AI module is simply a piece of software that communicates with an AI model to perform a particular task.

In this example, the Python program acts as the module.

Its responsibility is to:

1. Accept some source code.
2. Tell the AI what we want to know about that code.
3. Send the request to an AI model.
4. Receive the model's response.
5. Give that response back to the program.

The AI model does the actual language understanding, while Python handles the communication and program logic.

---

## 3. Why Use an API?

A Python program cannot automatically "think" like an AI model.

Instead, it communicates with an AI service through an **API**.

API stands for **Application Programming Interface**.

An API provides a defined way for one program to communicate with another service.

In this case:

```text
Python Program
     ↓
   API Request
     ↓
   AI Service
     ↓
   AI Model
     ↓
   API Response
     ↓
Python Program
```

The Python application sends information to the AI service and receives generated text in response.

---

## 4. The OpenAI Python Library

Writing HTTP requests manually every time we want to communicate with an AI service would be inconvenient.

The OpenAI Python package provides a client that makes this communication easier.

It can be installed using:

```bash
pip install openai
```

Then Python can import the client:

```python
from openai import OpenAI
```

The `OpenAI` class provides methods for communicating with compatible OpenAI API endpoints.

---

## 5. API Keys and Environment Variables

An API usually requires authentication.

An **API key** is a credential that identifies and authorizes the application making the request.

A key should generally not be written directly into source code like this:

```python
api_key = "my-secret-key"
```

If the code is uploaded to GitHub or shared with somebody else, the secret could be exposed.

A common solution is to store credentials in **environment variables**.

Python can read an environment variable using the `os` module:

```python
import os

api_key = os.environ.get("OPENAI_API_KEY")
```

The same idea can be used for the API base URL:

```python
base_url = os.environ.get("OPENAI_API_BASE")
```

This separates configuration and secrets from application code.

---

## 6. Creating the Client

Once the credentials are available, they can be supplied to the client:

```python
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)
```

Here:

- `api_key` provides authentication.
- `base_url` specifies the API endpoint.
- `client` becomes the object through which the program communicates with the AI service.

The important programming idea is that we create the client once and then use it when making requests.

---

## 7. Functions Make the Code Reusable

Instead of writing the AI request directly for one particular code snippet, we can put the logic inside a function.

For example:

```python
def generate_comment(code_snippet: str) -> str:
```

This function represents a reusable operation:

> "Give me some code, and I will give you a comment describing it."

The function accepts `code_snippet` as a parameter.

That means it can work with many different pieces of code.

For example:

```python
generate_comment(code1)
generate_comment(code2)
generate_comment(code3)
```

The function does not need to know beforehand what the code will be.

---

## 8. Type Hints

The function contains:

```python
code_snippet: str
```

and:

```python
-> str
```

These are Python **type hints**.

`code_snippet: str` tells the reader that `code_snippet` is expected to be a string.

`-> str` indicates that the function is expected to return a string.

Type hints do not change the basic purpose of the function. They mainly make code easier to understand, maintain, and analyze with development tools.

---

## 9. What is a Prompt?

A **prompt** is the instruction or input given to an AI model.

For this application, simply sending the code may not be enough.

We need to tell the model what we want it to do.

For example:

```text
Generate a clear, concise one-line comment explaining the purpose of this code.
```

The instruction tells the model what kind of output we expect.

A good prompt should clearly specify:

- What the AI should analyze.
- What it should produce.
- How the output should be formatted.
- Any limitations on the response.

---

## 10. Dynamic Prompts

The interesting part is that the code being analyzed changes.

Therefore, the prompt needs to be **dynamic**.

Python f-strings make this easy:

```python
prompt = f"""
Generate a clear, concise one-line comment explaining the purpose
of the following Python code.

Code:
{code_snippet}
"""
```

The `{code_snippet}` portion is replaced with the actual value supplied to the function.

For example, if the input is:

```python
def add(a, b):
    return a + b
```

the AI receives a prompt containing that code.

If another function is supplied, the prompt automatically changes.

This is why parameterization is important.

---

## 11. Why Prompt Instructions Matter

AI models generate responses based on the instructions and information provided to them.

Compare these two requests:

```text
Explain this code.
```

and:

```text
Generate a clear, concise one-line comment explaining the purpose
of this Python code. Return only the comment.
```

The second instruction is more specific about the desired output.

For an application, predictable output is useful because the program may want to directly use the generated text.

This is an example of **prompt engineering**: designing instructions that guide the model toward the desired result.

---

## 12. Chat Messages

The AI request uses a `messages` structure:

```python
messages=[
    {"role": "user", "content": prompt}
]
```

A message contains a role and content.

The `user` role represents the instruction being provided to the model.

The `content` contains the actual prompt.

Conceptually:

```text
Role: user
Content: "Generate a comment for this code..."
```

The API uses this structured format to represent the conversation sent to the model.

---

## 13. Choosing a Model

An AI service can provide multiple models, each designed for different capabilities and trade-offs.

The model specified for this exercise is:

```text
openai/gpt-4.1-mini
```

The model name tells the API which model should process the request.

Choosing a model is an important part of AI application development because different models can have different capabilities, latency, and cost characteristics.

---

## 14. Controlling the Response Length

The request includes:

```python
max_tokens=30
```

A token is a unit used by language models when processing text.

It is not exactly the same thing as a word or character.

For example, a short sentence may consist of several tokens.

Since the application only needs a short comment, limiting the generated output helps prevent unnecessarily long responses.

The value `30` is the maximum requested output length for this task.

---

## 15. Temperature

Another parameter is:

```python
temperature=0.2
```

Temperature influences how varied or random the model's output can be.

A lower value generally encourages more predictable and focused responses.

A higher value can produce more variation.

For a code-comment generator, we generally want a concise and consistent description rather than highly creative text, which is why a low temperature is appropriate here.

---

## 16. Understanding the API Response

After sending the request, the API returns a response object.

It is stored in:

```python
response
```

The generated message can be accessed through:

```python
response.choices[0].message.content
```

Conceptually, the response contains information similar to:

```text
Response
 └── choices
      └── first result
           └── message
                └── content
```

The `content` is the actual text generated by the model.

---

## 17. Why Use `.strip()`?

The generated content can sometimes contain unnecessary spaces or newline characters.

Using:

```python
comment = response.choices[0].message.content.strip()
```

removes whitespace from the beginning and end.

This gives the application a cleaner string.

---

## 18. Print vs Return

These two operations have different purposes:

```python
print(comment)
```

displays the result in the terminal.

Whereas:

```python
return comment
```

sends the result back to whatever code called the function.

For example:

```python
result = generate_comment(code)
```

After the function finishes, `result` can contain the generated comment.

A function can therefore both display a result and return it for further use.

---

## 19. The Complete Concept

The complete application can be understood as several layers:

```text
Python Function
      ↓
Build Dynamic Prompt
      ↓
OpenAI Client
      ↓
API Request
      ↓
Selected AI Model
      ↓
Generated Response
      ↓
Extract Text
      ↓
Print / Return
```

Each part has a separate responsibility.

Python handles the application logic.

The prompt describes the task.

The API provides communication with the AI service.

The model analyzes the code and generates natural language.

The response-processing code extracts the useful result.

---

## 20. Why This Pattern Is Useful

The same pattern can be used for many developer tools.

Instead of generating comments, an application could ask an AI model to:

- Explain a function.
- Generate documentation.
- Summarize a file.
- Generate unit tests.
- Suggest improvements.
- Convert code between languages.
- Find possible bugs.
- Generate commit messages.
- Explain error messages.

The main pattern remains similar:

```text
Input
  ↓
Prompt
  ↓
AI Model
  ↓
Response
  ↓
Application Output
```

---

## 21. Important Takeaways

The most important concepts from this exercise are:

**API** — a way for software to communicate with another service.

**API key** — a credential used to authenticate requests.

**Environment variable** — a way to provide configuration or secrets to an application without putting them directly in source code.

**OpenAI client** — a Python object used to communicate with the configured AI API.

**Prompt** — the instruction and information given to the AI model.

**Parameterization** — designing code so the input can change instead of hardcoding one specific value.

**Model** — the AI system that processes the prompt and generates a response.

**Temperature** — a setting that influences response variability.

**Tokens** — units used by language models to process and generate text.

**Response** — the data returned by the AI service after processing the request.

**Return value** — the result a Python function gives back to its caller.

---

## 22. The Bigger Picture

This small project demonstrates the foundation of building **AI-powered applications**.

The AI itself is not the entire application.

The application is responsible for:

- collecting input,
- preparing instructions,
- communicating with the model,
- processing the response,
- and presenting or using the result.

Understanding this separation is important because most real-world AI applications follow the same general architecture.

The model provides the intelligence, while the surrounding Python program provides the structure and behavior needed to turn that intelligence into a useful tool.


# Day 4 - AI Comparison Lab

## 1. Objective

The goal of this task is to build a small Python program that uses an OpenAI-compatible API to compare the chips used in two iPhone models.

The two models are:

- iPhone 13
- iPhone 17

The program must return the comparison result as **one word only**.

---

## 2. Project Structure

The project is located at:

```text
/root/openaiproject
```

Important files:

```text
openaiproject/
├── compare.py
├── day.md
├── notes.md
└── venv/
```

The `venv` directory contains the Python virtual environment and should not be uploaded to GitHub.

---

## 3. Python Virtual Environment

A virtual environment keeps the project's Python packages separate from the system Python installation.

Create and activate it with:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the OpenAI Python package:

```bash
pip install openai
```

---

## 4. API Configuration

The OpenAI API key and base URL are provided through environment variables.

The program reads them using:

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

The API key should **never be written directly into source code or committed to GitHub**.

The environment variables can be loaded from `/root/.bash_profile`:

```bash
source /root/.bash_profile
```

---

## 5. Creating the OpenAI Client

The OpenAI client is created using the API key and base URL:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)
```

`os` is used to access environment variables.

`OpenAI` creates the client used to communicate with the API.

---

## 6. The compare() Function

The required function accepts two parameters:

```python
def compare(item1: str, item2: str) -> str:
```

- `item1` is the first iPhone model.
- `item2` is the second iPhone model.
- `-> str` indicates that the function returns a string.

The prompt is parameterized, meaning the function can work with different items instead of having the model names permanently written into the prompt.

---

## 7. Prompt Design

The prompt tells the AI exactly what information to compare and how the answer should be formatted.

Example:

```python
prompt = (
    f"Compare the chips used in {item1} and {item2}. "
    "Return ONLY the chip name used in the second model. "
    "Output exactly one word. No explanation, no punctuation."
)
```

The important part is the explicit output instruction.

Without a strict format instruction, the model may return an explanation such as:

```text
The iPhone 13 uses the A15 Bionic chip.
The iPhone 17 uses the A17.
```

The task requires only:

```text
A17
```

---

## 8. Sending the Prompt to the Model

The prompt is sent using the chat completion API:

```python
response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=100,
    temperature=0.5
)
```

### Parameters

- `model` specifies the AI model.
- `messages` contains the conversation sent to the model.
- `role: "user"` identifies the message as the user's request.
- `content` contains the constructed prompt.
- `max_tokens=100` limits the maximum response length.
- `temperature=0.5` controls response variability.

---

## 9. Getting the Model's Answer

The returned answer is extracted with:

```python
response.choices[0].message.content.strip()
```

`strip()` removes unnecessary whitespace around the answer.

The function therefore returns:

```python
return response.choices[0].message.content.strip()
```

---

## 10. Complete compare.py

The completed program is:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)

def compare(item1: str, item2: str) -> str:
    prompt = (
        f"Compare the chips used in {item1} and {item2}. "
        "Return ONLY the chip name used in the second model. "
        "Output exactly one word. No explanation, no punctuation."
    )

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.5
    )

    return response.choices[0].message.content.strip()

response = compare("iphone 13", "iphone 17")
print(response)
```

---

## 11. Running the Program

Activate the virtual environment:

```bash
source venv/bin/activate
```

Make sure the environment variables are available:

```bash
source /root/.bash_profile
```

Run:

```bash
python compare.py
```

The completed execution produced:

```text
A17
```

---

## 12. Troubleshooting

### Model returns a full explanation

If the output contains multiple sentences, make the prompt stricter:

```text
Return ONLY the chip name used in the second model.
Output exactly one word.
No explanation, no punctuation.
```

### API key error

Check that the environment variable is available:

```bash
echo $OPENAI_API_KEY
```

Do not paste the key into `compare.py`.

### Module not found

If Python reports that `openai` cannot be found:

```bash
source venv/bin/activate
pip install openai
```

### Wrong Python environment

Check the active Python:

```bash
which python
```

It should point to the project's virtual environment.

---

## 13. GitHub Preparation

The virtual environment should not be committed because it contains installed packages and environment-specific files.

A suitable `.gitignore` is:

```gitignore
venv/
__pycache__/
.env
```

Add the project files:

```bash
git add compare.py day.md notes.md .gitignore
```

Create a commit:

```bash
git commit -m "Add AI chip comparison lab"
```

Push to GitHub:

```bash
git push
```

---

## 14. Key Concepts Learned

This exercise demonstrates:

- Python functions with parameters and return types.
- Environment variables for configuration and secrets.
- Creating an OpenAI-compatible client.
- Constructing parameterized prompts with f-strings.
- Sending user messages to a chat model.
- Controlling model output with `max_tokens` and `temperature`.
- Extracting text from an API response.
- Using a virtual environment.
- Running a Python program from the terminal.
- Preparing project files for GitHub.
- Keeping API credentials out of source control.

## Final Result

The AI comparison program successfully compared the requested iPhone models and produced the required one-word output:

```text
A17
```

---

# Day 5 - AI Converter

## 1. What is the task?

The goal is to build a small Python module that uses an AI model to convert a paragraph into concise, meaningful bullet points.

The input paragraph is:

> Artificial Intelligence is transforming industries by automating tasks, improving decision-making, and enabling new innovations across healthcare, finance, and education.

The program should send this paragraph to an OpenAI-compatible chat API and print the AI-generated bullet points.

---

## 2. Required Python setup

A virtual environment keeps the project's Python packages isolated from the system Python.

Create it with:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the OpenAI Python package:

```bash
pip install openai
```

It is important to activate the virtual environment before running the program. Otherwise, using `/usr/bin/python` may produce:

```text
ModuleNotFoundError: No module named 'openai'
```

The correct Python should be the one inside:

```text
/root/openaiproject/venv/bin/python
```

---

## 3. API credentials

The lab provides the API key and API base URL through `/root/.bash_profile`.

Load them with:

```bash
source /root/.bash_profile
```

The program reads them from environment variables:

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

This is preferable to placing the secret API key directly in the source code.

The client is created with:

```python
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)
```

The `base_url` is important because this lab uses an OpenAI-compatible service rather than necessarily using the standard OpenAI endpoint.

---

## 4. Checking available models

The task originally specifies:

```text
openai/gpt-4.1
```

However, model availability can change in the lab environment.

The environment provides an `ALLOWED_MODELS` variable:

```bash
echo "$ALLOWED_MODELS"
```

In this environment, the available list included:

```text
openai/gpt-4.1-mini
```

but did not include:

```text
openai/gpt-4.1
```

Therefore, `openai/gpt-4.1-mini` was used because it is an allowed model and the lab forum indicated that the grader accepts it.

The API model endpoint can also be checked:

```bash
curl -s "$OPENAI_API_BASE/models" \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

An empty result such as:

```json
{"object":"list","data":[]}
```

means that the endpoint is not currently advertising any models. In that situation, repeatedly running the script will not solve the problem.

---

## 5. The conversion function

The required function is:

```python
def convert_to_bullets(text: str) -> str:
```

It accepts exactly one parameter, `text`.

The type annotation:

```python
text: str
```

means the function expects a string.

The return annotation:

```python
-> str
```

means it returns a string containing the generated bullet points.

---

## 6. Parameterized prompt

The prompt must use the supplied paragraph dynamically rather than hardcoding the paragraph inside the prompt.

An f-string is used:

```python
prompt = f"""Convert the following paragraph into short, meaningful bullet points.
Keep the bullet points concise and easy to read.

Paragraph:
{text}
"""
```

The `{text}` placeholder is replaced with the actual argument passed to the function.

This makes the function reusable for different paragraphs.

---

## 7. Sending the request

The AI request uses the chat completions API:

```python
response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=150,
    temperature=0.1,
)
```

Important parameters:

- `model` selects the AI model.
- `messages` contains the conversation sent to the model.
- `role="user"` identifies the prompt as a user request.
- `content=prompt` sends the generated prompt.
- `max_tokens=150` limits the response length.
- `temperature=0.1` makes the output relatively consistent and focused.

The complete API result is stored in the required variable:

```python
response
```

---

## 8. Extracting the AI response

The actual generated text is obtained with:

```python
response.choices[0].message.content
```

The function returns this value:

```python
return response.choices[0].message.content
```

---

## 9. Running the conversion

The paragraph is assigned to `text`:

```python
text = """Artificial Intelligence is transforming industries by automating tasks, improving decision-making, and enabling new innovations across healthcare, finance, and education."""
```

Then the function is called:

```python
response = convert_to_bullets(text)
```

Finally, the result is printed:

```python
print(response)
```

This also satisfies the requirement to store the result in a variable named `response`.

---

## 10. Complete solution

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)

def convert_to_bullets(text: str) -> str:
    prompt = f"""Convert the following paragraph into short, meaningful bullet points.
Keep the bullet points concise and easy to read.

Paragraph:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.1,
    )

    return response.choices[0].message.content

text = """Artificial Intelligence is transforming industries by automating tasks, improving decision-making, and enabling new innovations across healthcare, finance, and education."""

response = convert_to_bullets(text)
print(response)
```

---

## 11. Execution

From the project directory:

```bash
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
python converter.py
```

The successful execution produced:

```text
- AI automates tasks across industries
- Enhances decision-making processes
- Drives innovations in healthcare, finance, and education
```

---

## 12. Important debugging lessons

### `ModuleNotFoundError`

If this command is used:

```bash
/usr/bin/python /root/openaiproject/converter.py
```

the system Python may not have the `openai` package installed.

Use the virtual environment instead:

```bash
source /root/openaiproject/venv/bin/activate
python converter.py
```

### `403 Model not supported`

If the API returns:

```text
403 - Model 'openai/gpt-4.1' is not supported.
```

the problem is model availability, not the Python installation.

Check:

```bash
echo "$ALLOWED_MODELS"
```

and use a model that the current lab environment permits when the lab's grading guidance allows it.

### Terminal paste errors

Errors such as:

```text
bash: ~curl: command not found
```

or:

```text
bash: $'\E[200~echo': command not found
```

are caused by accidentally pasting extra terminal characters. Type or paste the command starting directly with `curl` or `echo`.

---

## 13. Key concepts to remember

The main concepts demonstrated by this task are:

1. **Virtual environments** isolate Python dependencies.
2. **Environment variables** safely provide API configuration.
3. **OpenAI-compatible clients** can communicate with custom API endpoints using `base_url`.
4. **Parameterized prompts** make functions reusable.
5. **Chat completion messages** specify the user's request to the model.
6. **Model availability** depends on the current lab/API configuration.
7. **Type hints** such as `text: str -> str` document expected input and output.
8. The API result is stored in `response`, and the generated content is extracted from the response object.
9. Always verify the environment before spending limited API requests.

## Final result

The AI Converter successfully accepts a paragraph, sends a parameterized instruction to an allowed AI model, receives concise bullet points, and prints them to the console.


Here is a focused `notes.md` for **Day 6 – Use AI as an Email Assistant**, written like concise lecturer notes while covering the complete workflow.

# Day 6 - Use AI as an Email Assistant

## Introduction

In this task, we build a Python-based AI Email Assistant.

The purpose of the application is to take an informal email message and rewrite it into a polite and professional email using an OpenAI-compatible API.

For example:

```text
hey send me that report asap
```

can be transformed into:

```text
Could you please send me that report as soon as possible? Thank you.
```

The important concept is that Python handles the application logic, while the AI model performs the language rewriting.

---

## Objective

Build a Python program that:

1. Accepts email text as input.
2. Creates a professional rewriting prompt.
3. Sends the prompt to an AI chat model.
4. Receives the rewritten email.
5. Stores the result in `response`.
6. Prints the rewritten email.

---

## Step 1 - Project Directory

Move into the project directory:

```bash
cd /root/openaiproject
```

The required Python file is:

```text
/root/openaiproject/email_assistant.py
```

---

## Step 2 - Create Virtual Environment

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

A virtual environment keeps project dependencies isolated from the system Python installation.

---

## Step 3 - Load Environment Configuration

Load the provided API configuration:

```bash
source /root/.bash_profile
```

The program can access the API key and base URL through environment variables:

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

This avoids putting the API key directly into the source code.

---

## Step 4 - Install OpenAI Package

Install the Python OpenAI package:

```bash
pip install openai
```

The package provides the `OpenAI` client used to communicate with the API.

---

## Step 5 - Create the OpenAI Client

The required imports are:

```python
import os
from openai import OpenAI
```

Create the client:

```python
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)
```

Here:

- `api_key` retrieves the API key from the environment.
- `base_url` retrieves the API endpoint from the environment.
- `client` is used to send requests to the AI model.

---

## Step 6 - Create the Email Function

The function must accept exactly one parameter:

```python
def rewrite_email(text: str) -> str:
```

The `text` parameter contains the email that needs to be rewritten.

The `-> str` type hint indicates that the function returns a string.

---

## Step 7 - Create a Parameterized Prompt

Inside the function, create the prompt:

```python
prompt = f"""Rewrite the following email politely and professionally.
Preserve the original meaning while improving the tone and wording.

Email:
{text}
"""
```

The important part is:

```python
{text}
```

This makes the prompt parameterized.

Therefore, the same function can process different emails rather than being limited to one hardcoded message.

For example:

```text
Email:
hey send me that report asap
```

is automatically inserted into the prompt.

---

## Step 8 - Send the Prompt to the AI Model

Send the prompt using the chat completion API:

```python
response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=60,
    temperature=0.1,
)
```

### Model

```python
model="openai/gpt-4.1-mini"
```

The compatible model available for the environment is used.

### Messages

```python
messages=[
    {"role": "user", "content": prompt}
]
```

The prompt is sent as a user message.

### Max Tokens

```python
max_tokens=60
```

This limits the maximum amount of generated output.

Because the requested email is short, 60 tokens is sufficient.

### Temperature

```python
temperature=0.1
```

A low temperature makes the response more controlled and consistent, which is useful for professional rewriting.

---

## Step 9 - Extract the AI Response

The generated text can be accessed with:

```python
response.choices[0].message.content
```

The function returns this generated text:

```python
return response.choices[0].message.content.strip()
```

Using `.strip()` removes unnecessary whitespace around the response.

---

## Complete `email_assistant.py`

The complete program is:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)

def rewrite_email(text: str) -> str:
    prompt = f"""Rewrite the following email politely and professionally.
Preserve the original meaning while improving the tone and wording.

Email:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=60,
        temperature=0.1,
    )

    return response.choices[0].message.content.strip()

text = "hey send me that report asap"

response = rewrite_email(text)
print(response)
```

---

## Step 10 - Run the Program

Activate the virtual environment and load the environment configuration:

```bash
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
```

Run the program:

```bash
python email_assistant.py
```

---

## Input

The input email is:

```text
hey send me that report asap
```

This is informal and uses abbreviated language.

The AI is instructed to preserve the meaning while making the message polite and professional.

---

## Output

A suitable output is:

```text
Could you please send me that report as soon as possible? Thank you.
```

The meaning remains the same: the sender wants the report soon.

The wording is improved by:

- Using a polite request.
- Expanding informal wording.
- Removing the abrupt tone.
- Adding professional phrasing.

---

## How the Program Works

The complete flow is:

```text
Email Text
    ↓
rewrite_email()
    ↓
Parameterized Prompt
    ↓
OpenAI Client
    ↓
Chat Model
    ↓
response
    ↓
Generated Professional Email
    ↓
Console
```

Python does not manually rewrite the email. It provides the instructions and input to the AI model, receives the generated response, and displays it.

---

## Important Concepts

### Environment Variables

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

These allow configuration to be supplied externally instead of hardcoding credentials.

### Function

```python
def rewrite_email(text: str) -> str:
```

The function makes the solution reusable for different email messages.

### Parameterized Prompt

```python
{text}
```

The input text is dynamically inserted into the prompt.

### API Response

```python
response
```

The complete response returned by the model is stored in this variable.

### Generated Content

```python
response.choices[0].message.content
```

This accesses the actual text generated by the model.

---

## Key Takeaways

- The OpenAI Python package allows Python applications to communicate with an AI model.
- API credentials can be loaded from environment variables.
- Functions make AI functionality reusable.
- Parameterized prompts allow different emails to be processed.
- `max_tokens` controls the maximum response length.
- A low `temperature` helps produce consistent professional wording.
- The model performs the language transformation.
- Python receives and prints the generated result.

---

Absolutely — this should be **Day 7**, and based on the earlier task, it should cover the **AI Resume Extractor**, not the Email Assistant.

# Day 7 — AI Resume Extractor

## 1. Objective

The goal of Day 7 is to build a Python-based **AI Resume Extractor**.

The application receives a resume paragraph and uses an OpenAI-compatible AI model to extract exactly **five job-relevant keywords**.

For example, from:

```text
Experienced DevOps engineer skilled in Python, Kubernetes, Docker, CI/CD pipelines, and cloud automation.
```

the application should return five relevant keywords in comma-separated format.

The main function is:

```python
extract_keywords(text: str) -> str
```

---

## 2. Project Setup

Move into the project directory:

```bash
cd /root/openaiproject
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Load the environment variables:

```bash
source /root/.bash_profile
```

Install the OpenAI Python package:

```bash
pip install openai
```

### Why use a virtual environment?

A virtual environment keeps project dependencies isolated. This prevents packages installed for one project from interfering with another project.

---

## 3. API Configuration

The API key and API base URL are provided through environment variables.

They can be accessed using:

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

This avoids hardcoding sensitive credentials directly into the program.

---

## 4. Creating the OpenAI Client

First import the required modules:

```python
import os
from openai import OpenAI
```

Then create the client:

```python
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)
```

The client is responsible for communicating with the OpenAI-compatible API.

---

## 5. Creating the Extraction Function

The required function is:

```python
def extract_keywords(text: str) -> str:
```

Here:

- `text` contains the resume paragraph.
- `str` after the colon indicates the input type.
- `-> str` indicates that the function returns a string.

The function can therefore be reused with different resumes.

---

## 6. Building the Parameterized Prompt

The prompt must clearly tell the AI what to extract.

```python
prompt = f"""
Extract exactly 5 job-relevant keywords from the following resume text.

Requirements:
- Return exactly five keywords.
- Separate the keywords with commas.
- Do not include numbering, bullets, explanations, or any other text.
- Choose the most relevant technical/job-related keywords.

Resume text:
{text}
"""
```

This is a **parameterized prompt** because `{text}` is replaced with the actual resume content.

The most important instruction is:

```text
Return exactly five keywords.
```

The prompt also specifies that the keywords must be comma-separated.

---

## 7. Why Prompt Design Matters

The model needs explicit output instructions.

If we simply ask:

```text
Extract keywords from this resume.
```

the model might return a list, explanation, or more than five keywords.

Instead, the prompt establishes a strict output format:

```text
keyword1, keyword2, keyword3, keyword4, keyword5
```

This makes the AI output easier for a program to process.

---

## 8. Calling the AI Model

The model is called using:

```python
response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=40,
    temperature=0,
)
```

### Model

```text
openai/gpt-4.1-mini
```

This is the model specified for the task.

### Messages

The prompt is sent as a user message:

```python
messages=[
    {"role": "user", "content": prompt}
]
```

### max_tokens

```python
max_tokens=40
```

The output is short because we only need five keywords.

### temperature

```python
temperature=0
```

A temperature of zero makes the response as deterministic and consistent as possible.

This is useful when the application expects a specific output format.

---

## 9. Getting the Generated Keywords

The generated response is available through:

```python
response.choices[0].message.content
```

To remove unnecessary whitespace:

```python
response.choices[0].message.content.strip()
```

Therefore the function returns:

```python
return response.choices[0].message.content.strip()
```

---

## 10. Complete Function

The complete extraction function is:

```python
def extract_keywords(text: str) -> str:
    prompt = f"""
Extract exactly 5 job-relevant keywords from the following resume text.

Requirements:
- Return exactly five keywords.
- Separate the keywords with commas.
- Do not include numbering, bullets, explanations, or any other text.
- Choose the most relevant technical/job-related keywords.

Resume text:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=40,
        temperature=0,
    )

    return response.choices[0].message.content.strip()
```

---

## 11. Complete Program

The complete `/root/openaiproject/resume_extractor.py` file is:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)

def extract_keywords(text: str) -> str:
    prompt = f"""
Extract exactly 5 job-relevant keywords from the following resume text.

Requirements:
- Return exactly five keywords.
- Separate the keywords with commas.
- Do not include numbering, bullets, explanations, or any other text.
- Choose the most relevant technical/job-related keywords.

Resume text:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=40,
        temperature=0,
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    resume_text = (
        "Experienced DevOps engineer skilled in Python, Kubernetes, Docker, "
        "CI/CD pipelines, and cloud automation."
    )

    keywords = extract_keywords(resume_text)
    print(keywords)
```

---

## 12. Running the Program

Activate the virtual environment:

```bash
cd /root/openaiproject
source venv/bin/activate
```

Load the API configuration:

```bash
source /root/.bash_profile
```

Run the Python program:

```bash
python resume_extractor.py
```

---

## 13. Input Resume

The provided resume text is:

```text
Experienced DevOps engineer skilled in Python, Kubernetes, Docker, CI/CD pipelines, and cloud automation.
```

The AI should identify the most relevant job-related technologies and skills.

---

## 14. Expected Output Format

The output must contain exactly five comma-separated keywords.

For example:

```text
Python, Kubernetes, Docker, CI/CD, Cloud Automation
```

The exact keyword selection is determined by the AI, but the required format is:

```text
keyword1, keyword2, keyword3, keyword4, keyword5
```

There should be no numbering, bullets, or explanation.

---

## 15. Available Models

The allowed models can be checked with:

```bash
echo "$ALLOWED_MODELS"
```

The model used for this task is:

```text
openai/gpt-4.1-mini
```

---

## 16. Important Concepts

- **Resume extraction:** Converts unstructured resume text into useful job-related information.
- **AI model:** Understands the resume and identifies relevant skills.
- **Parameterized prompt:** Inserts the supplied resume dynamically into the prompt.
- **Exact output instruction:** Forces the model to produce five keywords.
- **Comma-separated output:** Provides a simple format that other software can process.
- **Temperature 0:** Makes the output more deterministic.
- **max_tokens 40:** Keeps the response short.
- **Environment variables:** Provide API credentials without hardcoding them.
- **Virtual environment:** Isolates the Python project's dependencies.

---

## 17. Overall Flow

The complete process can be remembered as:

```text
Resume text
    ↓
extract_keywords(text)
    ↓
Build parameterized prompt
    ↓
Send prompt to gpt-4.1-mini
    ↓
AI identifies job-relevant keywords
    ↓
Return exactly five comma-separated keywords
    ↓
Print keywords
```

## 18. Key Takeaway

The important lesson from Day 7 is how to use an AI model to convert **unstructured resume text into structured information**.

Python manages the application and API call, while the AI model performs the language understanding and keyword extraction.

The most important implementation requirements are:

```text
Function: extract_keywords
Input: resume text
Output: exactly 5 comma-separated keywords
Model: openai/gpt-4.1-mini
max_tokens: 40
temperature: 0
```

# Day 8 — AI Haiku Generator

## 1. Objective

The goal is to build a Python program that uses an OpenAI-compatible AI model to generate a **three-line haiku** from a given topic.

For this task, the topic is:

```text
sky
```

A haiku follows the traditional **5-7-5 syllable structure**:

- Line 1 → 5 syllables
- Line 2 → 7 syllables
- Line 3 → 5 syllables

The program should print only the generated three-line haiku.

## 2. Project Setup

Work inside:

```bash
cd /root/openaiproject
```

Create and activate a virtual environment so the project dependencies remain isolated:

```bash
python3 -m venv venv
source venv/bin/activate
```

The API configuration is provided through `/root/.bash_profile`, so load it with:

```bash
source /root/.bash_profile
```

Install the OpenAI Python package:

```bash
pip install openai
```

## 3. API Configuration

The OpenAI client needs two pieces of configuration:

- `OPENAI_API_KEY` → authentication key
- `OPENAI_API_BASE` → API endpoint

They can be read safely from environment variables:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)
```

Using environment variables avoids hardcoding the API credentials directly into the source code.

## 4. The `generate_haiku()` Function

The required function is:

```python
def generate_haiku(topic: str) -> str:
```

It accepts one parameter, `topic`, and returns the generated haiku as a string.

The prompt must be **parameterized**, meaning the supplied topic is inserted into the prompt rather than being permanently written into the function.

For example:

```python
parameterized_prompt = f"""
Generate a haiku about {topic}.

Requirements:
- Exactly three distinct lines.
- Line 1 must contain exactly 5 syllables.
- Line 2 must contain exactly 7 syllables.
- Line 3 must contain exactly 5 syllables.
- Output only the three lines of the haiku.
- Do not include a title, numbering, explanation, or extra text.
"""
```

Here, `{topic}` is replaced by the actual argument passed to the function.

## 5. Calling the AI Model

The required model is:

```text
openai/gpt-4.1-mini
```

The prompt is sent through the OpenAI chat-completions interface:

```python
result = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": parameterized_prompt}
    ],
    max_tokens=60,
    temperature=0.0,
)
```

Important settings:

- `model` selects the AI model.
- `messages` contains the user prompt.
- `max_tokens=60` limits the response length.
- `temperature=0.0` makes generation deterministic and reduces unnecessary variation.

## 6. Getting the Response

The generated text is obtained from the first choice:

```python
response = result.choices[0].message.content.strip()
```

The variable must be named `response`.

`.strip()` removes unnecessary whitespace from the beginning and end of the generated text.

The function then returns it:

```python
return response
```

## 7. Complete Program

The complete `/root/openaiproject/haiku_generator.py` should be:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)


def generate_haiku(topic: str) -> str:
    parameterized_prompt = f"""
Generate a haiku about {topic}.

Requirements:
- Exactly three distinct lines.
- Line 1 must contain exactly 5 syllables.
- Line 2 must contain exactly 7 syllables.
- Line 3 must contain exactly 5 syllables.
- Output only the three lines of the haiku.
- Do not include a title, numbering, explanation, or extra text.
"""

    result = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": parameterized_prompt}
        ],
        max_tokens=60,
        temperature=0.0,
    )

    response = result.choices[0].message.content.strip()
    return response


if __name__ == "__main__":
    response = generate_haiku("sky")
    print(response)
```

## 8. Running the Program

From the project directory:

```bash
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
python haiku_generator.py
```

The program calls:

```python
generate_haiku("sky")
```

and prints the returned response.

The final output should contain **three distinct lines**, such as:

```text
Blue sky spreads above
Soft clouds drift across the blue
Sun warms earth below
```

The actual output is generated by the AI model.

## 9. Important Points to Remember

- The function must accept exactly one parameter: `topic`.
- The prompt must use the supplied topic dynamically.
- The haiku must have three lines.
- The required syllable pattern is **5-7-5**.
- The model is `openai/gpt-4.1-mini`.
- `max_tokens` must be `60`.
- `temperature` must be `0.0`.
- Store the generated content in `response`.
- Print the generated haiku.
- API credentials should come from environment variables.
- The work should be performed inside `/root/openaiproject`.
- The virtual environment should be activated before running the program.

## 10. What This Task Teaches

This task demonstrates the basic workflow for an AI-powered Python application:

**Python function → parameterized prompt → OpenAI-compatible API → model response → formatted output**

The important programming concepts are environment variables, virtual environments, Python functions, f-strings, API clients, structured API responses, and prompt design.

---

Below is a concise but **lecturer-style `notes.md`** covering the concepts, workflow, code, parameters, environment variables, API call, and important details without becoming unnecessarily large.

# Day 9 — AI Summarizer Notes

## 1. What Are We Building?

The goal is to build a simple **AI Summarizer** using Python and an OpenAI-compatible API.

The application takes a paragraph as input and asks an AI model to convert it into a **short, clear, single-line summary**.

The important concepts demonstrated are:

- Creating an OpenAI client
- Reading API configuration from environment variables
- Creating a reusable Python function
- Building a parameterized prompt
- Sending a prompt to a chat model
- Reading the model response
- Printing the generated result

---

## 2. Project Directory

The project is located at:

```bash
/root/openaiproject
```

Always move into the project directory before working:

```bash
cd /root/openaiproject
```

This ensures that files such as `summarizer.py` are created in the expected location.

---

## 3. Virtual Environment

A virtual environment keeps the Python packages for this project isolated from the system Python installation.

Create it with:

```bash
python3 -m venv venv
```

Activate it with:

```bash
source venv/bin/activate
```

After activation, Python and installed packages will use this project's virtual environment.

---

## 4. API Configuration

The API configuration is stored in:

```bash
/root/.bash_profile
```

Load it with:

```bash
source /root/.bash_profile
```

The important environment variables are:

```text
OPENAI_API_KEY
OPENAI_API_BASE
```

We can read them from Python using:

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

This is preferable to putting credentials directly into the Python source code.

---

## 5. Installing the OpenAI Package

The Python OpenAI package is required to communicate with the OpenAI-compatible API.

Install it using:

```bash
pip install openai
```

The package provides the `OpenAI` client used by our Python program.

---

## 6. Creating the OpenAI Client

First import the required modules:

```python
import os
from openai import OpenAI
```

Then create the client:

```python
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)
```

### What is happening here?

`OpenAI` creates the API client.

`api_key` provides authentication.

`base_url` tells the client which OpenAI-compatible API endpoint to use.

Instead of hardcoding these values, the program retrieves them from environment variables.

---

## 7. The `summarize()` Function

The main functionality is placed inside:

```python
def summarize(text: str) -> str:
```

This function has:

- `text: str` — the input paragraph
- `-> str` — the function returns a string

Using a function makes the summarizer reusable. We can provide different paragraphs without changing the API logic.

---

## 8. Parameterized Prompt

The prompt must contain the paragraph supplied to the function.

We can use an f-string:

```python
prompt = f"""
Summarize the following paragraph into a single-line summary.

Paragraph:
{text}

Requirements:
- Output exactly one line.
- Keep the summary concise and easy to understand.
- Capture the main idea of the paragraph.
- Do not include a title, numbering, explanation, or extra text.
"""
```

The important part is:

```python
{text}
```

This makes the prompt **parameterized**.

If `text` contains a different paragraph, the prompt automatically changes.

For example:

```python
text = "Artificial Intelligence enables machines to mimic human intelligence..."
```

will cause that paragraph to be inserted into the prompt.

---

## 9. Why Give Instructions in the Prompt?

The AI model can generate many different forms of answers.

Our requirement is specifically a **single-line summary**, so the prompt gives the model clear instructions.

The important instructions are:

- Summarize the paragraph
- Keep it concise
- Capture the main idea
- Return exactly one line
- Do not add explanations or extra text

Clear prompts help the model produce output closer to the required format.

---

## 10. Calling the Chat Model

The AI request is made with:

```python
result = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=60,
    temperature=0.5,
)
```

There are several important parameters here.

### Model

```python
model="openai/gpt-4.1-mini"
```

This specifies the AI model that should process the request.

### Messages

```python
messages=[
    {"role": "user", "content": prompt}
]
```

The model receives the prompt as a user message.

The `role` is:

```text
user
```

The actual prompt is passed through:

```python
content=prompt
```

### Maximum Tokens

```python
max_tokens=60
```

This limits the amount of output generated by the model.

Since we only need a short summary, 60 tokens is sufficient.

### Temperature

```python
temperature=0.5
```

Temperature controls the randomness of the model's output.

A value of `0.5` allows some variation while keeping the response relatively focused.

---

## 11. Reading the Model Response

The API returns a response object.

The generated text can be accessed with:

```python
result.choices[0].message.content
```

We remove unnecessary whitespace using:

```python
response = result.choices[0].message.content.strip()
```

The variable `response` therefore contains the generated summary.

The `.strip()` method removes leading and trailing whitespace.

---

## 12. Returning the Summary

The function returns the generated text:

```python
return response
```

Therefore:

```python
summarize(text)
```

returns a string containing the AI-generated summary.

---

## 13. Main Program

The script can use:

```python
if __name__ == "__main__":
```

This means the following code runs when the Python file is executed directly.

The paragraph is stored in:

```python
text = (
    "Artificial Intelligence enables machines to mimic human intelligence, "
    "performing tasks such as learning, problem-solving, and decision-making "
    "with increasing accuracy."
)
```

Then the summarizer is called:

```python
response = summarize(text)
```

Finally, the result is displayed:

```python
print(response)
```

---

## 14. Complete Program

The complete `summarizer.py` file is:

```python
import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)


def summarize(text: str) -> str:
    prompt = f"""
Summarize the following paragraph into a single-line summary.

Paragraph:
{text}

Requirements:
- Output exactly one line.
- Keep the summary concise and easy to understand.
- Capture the main idea of the paragraph.
- Do not include a title, numbering, explanation, or extra text.
"""

    result = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=60,
        temperature=0.5,
    )

    response = result.choices[0].message.content.strip()
    return response


if __name__ == "__main__":
    text = (
        "Artificial Intelligence enables machines to mimic human intelligence, "
        "performing tasks such as learning, problem-solving, and decision-making "
        "with increasing accuracy."
    )

    response = summarize(text)
    print(response)
```

---

## 15. Running the Program

Before running the program, activate the environment and load the API configuration:

```bash
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
```

Then run:

```bash
python summarizer.py
```

The program sends **one API request** and prints the generated summary.

The task allows a maximum of 10 requests, so unnecessary test requests should be avoided.

---

## 16. Expected Behavior

The input paragraph is:

```text
Artificial Intelligence enables machines to mimic human intelligence, performing tasks such as learning, problem-solving, and decision-making with increasing accuracy.
```

The model should produce a concise one-line summary similar to:

```text
AI enables machines to perform human-like tasks such as learning, problem-solving, and decision-making.
```

The exact wording can vary because the summary is generated by the AI model.

---

## 17. Important Concepts to Remember

### Environment Variables

Environment variables keep configuration and credentials outside the source code.

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

### Parameterized Prompt

The input is dynamically inserted into the prompt:

```python
{text}
```

This allows the same function to summarize different paragraphs.

### Function

The reusable interface is:

```python
summarize(text: str) -> str
```

It accepts text and returns a summary.

### Model

The required model is:

```text
openai/gpt-4.1-mini
```

### Chat Message

The prompt is sent as a user message:

```python
{"role": "user", "content": prompt}
```

### Output Limit

```python
max_tokens=60
```

This keeps the generated answer short.

### Temperature

```python
temperature=0.5
```

This controls response variability.

### Response

The generated text is extracted with:

```python
result.choices[0].message.content.strip()
```

and stored in:

```python
response
```

---

## 18. Execution Flow

The entire application follows this sequence:

```text
Start
  ↓
Move to /root/openaiproject
  ↓
Activate virtual environment
  ↓
Load API configuration
  ↓
Create OpenAI client
  ↓
Call summarize(text)
  ↓
Build parameterized prompt
  ↓
Send prompt to gpt-4.1-mini
  ↓
Receive model response
  ↓
Extract generated text
  ↓
Store it in response
  ↓
Print summary
  ↓
End
```

---

## 19. Key Requirements Checklist

- [x] Work directory: `/root/openaiproject`
- [x] Virtual environment created
- [x] OpenAI package installed
- [x] API configuration loaded from `/root/.bash_profile`
- [x] `OPENAI_API_KEY` used for the API key
- [x] `OPENAI_API_BASE` used for the API base URL
- [x] OpenAI client created
- [x] Function named `summarize`
- [x] Function signature: `summarize(text: str) -> str`
- [x] Prompt parameterized with the input paragraph
- [x] Model: `openai/gpt-4.1-mini`
- [x] Message role: `user`
- [x] Prompt passed as message content
- [x] `max_tokens=60`
- [x] `temperature=0.5`
- [x] API result stored in `response`
- [x] Summary printed to the terminal
- [x] Output requested as a single-line summary

## 20. Main Takeaway

This exercise demonstrates the basic pattern used in many AI applications:

**Input → Prompt → AI Model → Response → Application Output**

The Python program separates the AI functionality into a reusable `summarize()` function, dynamically inserts the user's text into a prompt, sends that prompt to an OpenAI-compatible model, extracts the generated response, and prints the result.

This same pattern can later be extended to applications such as issue summarization, document processing, support-ticket analysis, and developer-assistant tools.

---

# Day 10 Notes — AI Translator with OpenAI API

## 1. What We Are Building

In this task, we build a simple **AI Translator** using Python and an OpenAI-compatible API.

The program will:

- Accept English text.
- Accept a target language.
- Build a parameterized prompt.
- Send the prompt to `openai/gpt-4.1-mini`.
- Return the translated text.
- Translate the same sentence into Spanish and French.

The input used in this task is:

```text
Good morning, how are you?
```

---

## 2. Project Directory

All work is done inside:

```bash
cd /root/openaiproject
```

This keeps the project files and virtual environment together.

---

## 3. Virtual Environment

A virtual environment keeps the Python packages for this project isolated from the system Python installation.

Create it with:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Once activated, packages such as `openai` are installed inside this environment.

---

## 4. Install the OpenAI Package

Install the Python OpenAI SDK:

```bash
pip install openai
```

This provides the `OpenAI` class that Python uses to communicate with the API.

---

## 5. API Configuration

The API key and API base URL are provided through the environment.

Load the configuration:

```bash
source /root/.bash_profile
```

The values can be accessed in Python using:

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

Using environment variables is preferable to putting credentials directly into the source code.

---

## 6. Creating the OpenAI Client

First import the required modules:

```python
import os
from openai import OpenAI
```

Then create the client:

```python
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)
```

Here:

- `api_key` authenticates the request.
- `base_url` tells the SDK which OpenAI-compatible API endpoint to use.
- `client` is then used to make model requests.

---

## 7. Creating a Parameterized Function

The main function is:

```python
def translate_to_language(text: str, language: str) -> str:
```

The function accepts two parameters:

- `text` — the English text to translate.
- `language` — the target language.

The `-> str` indicates that the function returns a string.

This makes the translator reusable instead of hardcoding one particular sentence or language.

---

## 8. Building the Prompt

The prompt must be parameterized.

For example:

```python
prompt = f"Translate the following English text into {language}:\n\n{text}"
```

The `f` before the string allows Python variables to be inserted into the prompt.

If:

```python
text = "Good morning, how are you?"
language = "Spanish"
```

the resulting prompt becomes:

```text
Translate the following English text into Spanish:

Good morning, how are you?
```

The same function can therefore be used for French, Spanish, German, or another language.

---

## 9. Sending the Request

The model request is made with:

```python
response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=100,
    temperature=0.7,
)
```

Important parameters:

### `model`

```text
openai/gpt-4.1-mini
```

This specifies the AI model used for translation.

### `messages`

```python
messages=[
    {"role": "user", "content": prompt}
]
```

The parameter contains the conversation messages. Here, the generated prompt is sent as a **user** message.

### `max_tokens`

```python
max_tokens=100
```

Limits the amount of output generated by the model.

### `temperature`

```python
temperature=0.7
```

Controls the randomness of the generated response. A moderate value is suitable for natural language translation.

---

## 10. Extracting the Translation

The model response contains the generated message.

We extract its content using:

```python
response.choices[0].message.content.strip()
```

The `strip()` removes unnecessary whitespace around the response.

The function then returns the translated text:

```python
return response.choices[0].message.content.strip()
```

---

## 11. Calling the Function

The input is:

```python
text = "Good morning, how are you?"
```

Translate it into Spanish:

```python
spanish = translate_to_language(text, "Spanish")
```

Translate it into French:

```python
french = translate_to_language(text, "French")
```

Finally, print both results:

```python
print("Spanish:", spanish)
print("French:", french)
```

A typical result is:

```text
Spanish: Buenos días, ¿cómo estás?
French: Bonjour, comment ça va ?
```

The exact wording can vary because the response is generated by the AI model.

---

## 12. Complete Program

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE"),
)

def translate_to_language(text: str, language: str) -> str:
    prompt = f"Translate the following English text into {language}:\n\n{text}"

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    text = "Good morning, how are you?"

    spanish = translate_to_language(text, "Spanish")
    french = translate_to_language(text, "French")

    print("Spanish:", spanish)
    print("French:", french)
```

---

## 13. Running the Program

Make sure the environment and API configuration are loaded:

```bash
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
```

Run:

```bash
python translator.py
```

The program makes two model calls: one for Spanish and one for French.

---

## 14. Important Concepts Learned

### Parameterized Prompt

Instead of writing a fixed prompt, variables are inserted dynamically:

```python
f"Translate ... into {language} ... {text}"
```

This makes the function reusable.

### Environment Variables

Credentials are retrieved with:

```python
os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_BASE")
```

This avoids hardcoding API configuration in the program.

### OpenAI Client

The `OpenAI` class creates the client used to communicate with the OpenAI-compatible API.

### Model Request

The client sends the prompt using:

```python
client.chat.completions.create(...)
```

### Response Extraction

The generated text is obtained from:

```python
response.choices[0].message.content
```

---

## 15. Final Flow

The complete flow is:

```text
English text
     ↓
translate_to_language(text, language)
     ↓
Parameterized prompt
     ↓
OpenAI client
     ↓
openai/gpt-4.1-mini
     ↓
Generated translation
     ↓
Print result
```

## Key Takeaway

The main lesson is how to combine **Python functions, parameterized prompts, environment-based API configuration, and an OpenAI-compatible model** to build a reusable AI translation application.