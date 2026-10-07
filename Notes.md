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

# Day 11 Notes — AI Sentiment Classifier with Gemini API

## 1. What We Are Building

In this task, we build a simple **AI Sentiment Classifier** using Python and the Gemini API.

The program will:

- Accept a customer review.
- Build a parameterized prompt.
- Send the review to an AI model.
- Classify the review as Positive, Neutral, or Negative.
- Provide a short explanation.
- Print the sentiment and explanation to the console.

The first input used in this task is:

```text
The product arrived quickly and works perfectly.
```

---

## 2. Project Directory

Unlike the previous KodeKloud labs, Day 11 is part of my own AI Engineering practice project.

The project is located at:

```bash
cd /d/AI-KodeKloud
```

The Day 11 implementation is inside:

```text
Practice-Lab/
└── Day-11/
    └── sentiment_classifier.py
```

The project structure is:

```text
AI-KodeKloud/
├── Day1 - ...
├── Day2 - ...
├── ...
├── Day10 - ...
├── Day11 - AI Sentiment Classifier.md
│
├── Practice-Lab/
│   └── Day-11/
│       └── sentiment_classifier.py
│
├── Notes.md
├── README.md
└── venv/
```

The `venv` directory is local to the development environment and should not be pushed to GitHub.

---

## 3. Virtual Environment

A virtual environment keeps the Python packages for this project isolated from the system Python installation.

Create it with:

```bash
python3 -m venv venv
```

Because this project is being developed on Windows using Git Bash, the virtual environment is activated with:

```bash
source venv/Scripts/activate
```

After activation, the terminal shows:

```text
(venv)
```

This confirms that the virtual environment is active.

---

## 4. Installing the Gemini SDK

The Day 11 lab uses Google's Gemini API instead of the OpenAI API used in the previous KodeKloud labs.

Install the Gemini Python SDK:

```bash
pip install google-genai
```

The package provides the `google.genai` module used to create the Gemini client and send model requests.

---

## 5. API Configuration

For this self-created lab, I do not use the KodeKloud API configuration.

Instead, the Gemini API key is stored in an environment variable:

```text
GEMINI_API_KEY
```

In Git Bash, the API key can be set with:

```bash
export GEMINI_API_KEY="your-api-key"
```

The application reads the key using:

```python
import os

api_key = os.environ.get("GEMINI_API_KEY")
```

The API key should never be written directly into the Python source code.

It should also never be committed to GitHub.

---

## 6. Creating the Gemini Client

First import the required modules:

```python
import os

from google import genai
```

Then create the Gemini client:

```python
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)
```

Here:

- `GEMINI_API_KEY` contains the API credential.
- `os.environ.get()` reads the value from the environment.
- `client` is used to communicate with the Gemini API.

Using an environment variable keeps the API key separate from the source code.

---

## 7. Creating a Parameterized Function

The main function is:

```python
def classify_sentiment(review: str) -> str:
```

The function accepts one parameter:

- `review` — the customer review that needs to be analyzed.

The `-> str` indicates that the function returns a string.

The function is parameterized so that different customer reviews can be analyzed without changing the function itself.

For example:

```python
classify_sentiment("The product is excellent.")
```

and:

```python
classify_sentiment("The application crashes every time.")
```

can use the same function.

---

## 8. Building the Prompt

The prompt must use the review dynamically.

The basic structure is:

```python
prompt = f"""
Classify the following customer review as exactly one of:
Positive, Neutral, or Negative.

Also provide a short explanation.

Review:
{review}

Return the result in this format:

Sentiment: <Positive|Neutral|Negative>
Explanation: <short explanation>
"""
```

The `f` before the string allows the `review` variable to be inserted dynamically.

If:

```python
review = "The product arrived quickly and works perfectly."
```

the AI receives a prompt containing that review.

This makes the classifier reusable for different customer reviews.

---

## 9. Sending the Request

The Gemini model request is made with:

```python
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
)
```

Important parameters:

### `model`

```text
gemini-3.8-flash
```

This specifies the Gemini model used for the classification task.

The model name can change over time. If the API reports that a model is unavailable, the currently available Gemini model should be checked.

### `contents`

```python
contents=prompt
```

The parameterized prompt is sent to the Gemini model.

### `response`

The generated AI response is stored in:

```python
response
```

The generated text can then be accessed using:

```python
response.text
```

---

## 10. Returning the AI Response

The function returns the generated response:

```python
return response.text.strip()
```

The `strip()` method removes unnecessary whitespace from the beginning and end of the response.

The function therefore returns the AI-generated sentiment and explanation as a string.

---

## 11. Calling the Function

The first test review is:

```python
review = "The product arrived quickly and works perfectly."
```

The classifier is called with:

```python
response = classify_sentiment(review)
```

The result is then printed:

```python
print(response)
```

A successful result was:

```text
Sentiment: Positive
Explanation: The customer expresses complete satisfaction with both the fast shipping and the flawless performance of the product.
```

The exact explanation can vary because it is generated by the AI model.

---

## 12. Complete Program

```python
import os

from google import genai


client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


def classify_sentiment(review: str) -> str:
    prompt = f"""
Classify the following customer review as exactly one of:
Positive, Neutral, or Negative.

Also provide a short explanation.

Review:
{review}

Return the result in this format:

Sentiment: <Positive|Neutral|Negative>
Explanation: <short explanation>
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    return response.text.strip()


if __name__ == "__main__":
    review = "The product arrived quickly and works perfectly."

    response = classify_sentiment(review)

    print(response)
```

---

## 13. Running the Program

From the project root:

```bash
cd /d/AI-KodeKloud
```

Activate the virtual environment:

```bash
source venv/Scripts/activate
```

Set the API key if it is not already available:

```bash
export GEMINI_API_KEY="your-api-key"
```

Run the Day 11 application:

```bash
python Practice-Lab/Day-11/sentiment_classifier.py
```

Alternatively, enter the Day 11 directory:

```bash
cd Practice-Lab/Day-11
```

and run:

```bash
python sentiment_classifier.py
```

---

## 14. Testing

I tested the application with the following customer reviews.

### Test 1 — Positive

Input:

```text
The product arrived quickly and works perfectly.
```

Result:

```text
Sentiment: Positive
Explanation: The customer expresses complete satisfaction with both the fast shipping and the flawless performance of the product.
```

---

### Test 2 — Positive

Input:

```text
I absolutely love this product. It works perfectly!
```

Expected sentiment:

```text
Positive
```

---

### Test 3 — Neutral

Input:

```text
The product works as expected.
```

Expected sentiment:

```text
Neutral
```

---

### Test 4 — Negative

Input:

```text
The application crashes every time I open it.
```

Expected sentiment:

```text
Negative
```

---

### Test 5 — Mixed Sentiment

Input:

```text
The product is good, but delivery was very late.
```

This test is useful because the review contains both positive and negative information.

The result demonstrates how the AI handles a more ambiguous customer review.

---

## 15. Problem Encountered

Initially, the program used:

```python
model="gemini-2.5-flash"
```

The API returned:

```text
404 NOT_FOUND
```

with a message indicating that the model was no longer available to new users and recommending a newer model.

The model was changed to:

```python
model="gemini-3.8-flash"
```

After making this change, the program successfully generated the sentiment classification.

---

## 16. Understanding the Error

The error was:

```text
google.genai.errors.ClientError: 404 NOT_FOUND
```

This was not caused by an incorrect Python function or a missing API key.

The API request reached the Gemini service, but the requested model was not available for the account.

The important troubleshooting process was:

```text
API Request
     ↓
404 NOT_FOUND
     ↓
Check error message
     ↓
Identify unavailable model
     ↓
Change model
     ↓
Run again
     ↓
Successful response
```

This demonstrated the importance of reading API error messages instead of immediately rewriting the application.

---

## 17. AFC Warning

When the application was first executed, the SDK displayed a warning similar to:

```text
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended.
```

This was a warning rather than the cause of the failed request.

The actual failure was the `404 NOT_FOUND` model availability error.

After changing the model, the application successfully completed the request.

For this basic sentiment classification exercise, no explicit function-calling tools were being used.

---

## 18. Important Concepts Learned

### AI Classification

The model can classify natural-language input into predefined categories.

In this lab:

```text
Positive
Neutral
Negative
```

are the allowed sentiment categories.

---

### Parameterized Prompts

The review is inserted dynamically into the prompt:

```python
{review}
```

This allows the same function to process different customer reviews.

---

### Environment Variables

The API key is retrieved with:

```python
os.environ.get("GEMINI_API_KEY")
```

This keeps the credential outside the Python source code.

---

### AI Client

The Gemini client is created with:

```python
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)
```

The client handles communication with the Gemini API.

---

### Model Request

The model is called using:

```python
client.models.generate_content(...)
```

The prompt is passed using:

```python
contents=prompt
```

---

### Response Handling

The generated text is obtained from:

```python
response.text
```

and returned using:

```python
return response.text.strip()
```

---

## 19. Stretch Challenge

The next step is to process multiple customer reviews.

For example:

```text
Review 1: Great product and excellent service.
Review 2: The product works as expected.
Review 3: The application keeps crashing.
```

The program could classify each review and produce a summary such as:

```text
Positive: X
Neutral: X
Negative: X
```

where `X` represents the number of reviews assigned to each category.

---

## 20. Further Challenge

Add a model-generated confidence description.

For example:

```text
Sentiment: Positive
Confidence: High
Explanation: The customer clearly expresses satisfaction.
```

The confidence value should be treated as a model-generated signal rather than a statistically calibrated probability.

---

## 21. Security

The API key must not be stored in the Python source code.

Avoid:

```python
client = genai.Client(
    api_key="actual-api-key"
)
```

Instead use:

```python
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)
```

The API key should also not be added to GitHub.

The `.gitignore` file should contain:

```gitignore
venv/
__pycache__/
.env
```

Before committing the project, check:

```bash
git status
```

and make sure no credential files or virtual-environment files are being committed.

---

## 22. Final Flow

The complete application flow is:

```text
Customer Review
      ↓
classify_sentiment(review)
      ↓
Parameterized Prompt
      ↓
Gemini Client
      ↓
Gemini Flash Model
      ↓
AI Classification
      ↓
Sentiment + Explanation
      ↓
Print Result
```

---

## 23. Key Takeaway

The main lesson from Day 11 is how to build a simple **AI-powered classification application** using Python and a Gemini API.

I learned how to:

- Create a Python virtual environment.
- Install an AI SDK.
- Configure an API key using an environment variable.
- Create a Gemini client.
- Build a parameterized prompt.
- Pass dynamic user input to an AI model.
- Ask an AI model to classify text.
- Process the model response.
- Troubleshoot a model availability error.
- Test the application with different types of customer reviews.
- Keep API credentials out of source control.

The overall AI application pattern is:

```text
Input
  ↓
Python Function
  ↓
Parameterized Prompt
  ↓
AI Model
  ↓
AI Response
  ↓
Application Output
```

This pattern will be reused and expanded in future AI Engineering labs.

---
# Day 12 Notes — AI Data Analyzer with Gemini API

## 1. What We Are Building

In this task, we build a Python-based **AI Data Analyzer** using the Gemini API.

The application accepts a small employee dataset and asks an AI model to analyze the data and return structured JSON.

The dataset contains:

```text
Employee, Department, Salary, Experience
Rahul, IT, 85000, 5
Priya, HR, 65000, 4
Arun, IT, 95000, 7
Sneha, Finance, 72000, 6
```

The analysis includes:

- Total employees
- Highest salary employee
- Average salary
- Departments
- Average experience

---

## 2. Project Directory

The Day 12 implementation is located at:

```text
Practice-Lab/
└── Day-12/
    ├── data_analyzer.py
    └── README.md
```

---

## 3. Virtual Environment

The project uses the virtual environment created for the AI-KodeKloud repository.

Activate it using Git Bash:

```bash
cd /d/AI-KodeKloud
source venv/Scripts/activate
```

---

## 4. Gemini SDK

The Gemini Python SDK is installed using:

```bash
pip install google-genai
```

The application uses:

```python
from google import genai
```

---

## 5. API Configuration

The Gemini API key is stored in the environment variable:

```text
GEMINI_API_KEY
```

It is accessed from Python using:

```python
os.environ.get("GEMINI_API_KEY")
```

The API key is not stored directly in the source code.

---

## 6. Creating the Gemini Client

The client is created using:

```python
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)
```

The client is used to send the dataset and prompt to the Gemini model.

---

## 7. Data Analyzer Function

The main function is:

```python
def analyze_data(data: str) -> str:
```

The function accepts the dataset dynamically.

This makes it possible to analyze different datasets without changing the function itself.

---

## 8. Parameterized Prompt

The dataset is inserted dynamically into the prompt:

```python
prompt = f"""
Analyze the following employee dataset.

...

Employee dataset:

{data}
"""
```

The `data` parameter contains the employee information.

This creates a reusable AI data-analysis function.

---

## 9. Structured Output

The AI is instructed to return JSON with exactly these fields:

```json
{
  "total_employees": 4,
  "highest_salary_employee": "Arun",
  "average_salary": 79250,
  "departments": ["IT", "HR", "Finance"],
  "average_experience": 5.5
}
```

This is different from the previous sentiment classification lab because the application now expects structured information from the model.

---

## 10. Sending the Request

The Gemini request is made using:

```python
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
)
```

The generated response is stored in:

```python
response
```

The generated text is accessed using:

```python
response.text
```

---

## 11. JSON Parsing

Python provides the `json` module for working with JSON data.

It can be imported using:

```python
import json
```

A JSON response can be converted into a Python object using:

```python
result = json.loads(response)
```

Individual fields can then be accessed:

```python
result["total_employees"]
```

For example:

```python
print(result["average_salary"])
```

---

## 12. Expected Analysis

For the provided dataset:

```text
Employee, Department, Salary, Experience
Rahul, IT, 85000, 5
Priya, HR, 65000, 4
Arun, IT, 95000, 7
Sneha, Finance, 72000, 6
```

The expected values are:

```text
Total employees: 4
Highest salary employee: Arun
Average salary: 79250
Departments: IT, HR, Finance
Average experience: 5.5
```

---

## 13. Running the Application

From the project root:

```bash
cd /d/AI-KodeKloud
source venv/Scripts/activate
```

Set the API key:

```bash
export GEMINI_API_KEY="your-api-key"
```

Run:

```bash
python Practice-Lab/Day-12/data_analyzer.py
```

---

## 14. Important Concepts Learned

### Structured AI Output

The AI is instructed to return a predictable JSON structure instead of free-form text.

### Parameterized Prompts

The dataset is passed into the prompt dynamically.

### JSON

JSON allows the AI response to be consumed as structured data by Python.

### Environment Variables

The API key is kept outside the source code.

### AI + Python

The AI generates the analysis while Python can process the resulting structured information.

---

## 15. AI Analysis vs Python Analysis

This lab also introduces an important engineering consideration.

AI can be asked to perform numerical calculations:

```text
Dataset
   ↓
AI
   ↓
Calculations
```

However, Python can perform deterministic calculations:

```text
Dataset
   ↓
Python
   ↓
Calculations
```

A production application may use Python for exact numerical calculations and AI for tasks such as summarization or interpretation.

This is an important distinction when building reliable AI applications.

---

## 16. Final Flow

```text
Employee Dataset
       ↓
Parameterized Prompt
       ↓
Gemini API
       ↓
Gemini Flash
       ↓
Structured JSON
       ↓
Python JSON Processing
       ↓
Application Output
```

---

# Day 13 - AI Incident Entity Extractor

## 1. Introduction

The application takes an unstructured IT incident description and asks Gemini to extract important operational information into structured JSON.

For example:

```text
The production payment API started returning 503 errors
in the AWS Mumbai region at 10:30 AM. The issue affected
the ECS payment service and approximately 200 users.
The incident was classified as high severity.
```

Instead of manually reading this text, our AI application extracts:

```json
{
  "environment": "Production",
  "service": "Payment API",
  "cloud": "AWS",
  "region": "Mumbai",
  "platform": "ECS",
  "error": "503",
  "start_time": "10:30 AM",
  "affected_users": 200,
  "severity": "High"
}
```

The main idea is:

```text
Unstructured Text
       ↓
      Gemini
       ↓
Entity Extraction
       ↓
Structured JSON
```

---

# 2. What Is Entity Extraction?

Entity extraction means identifying specific pieces of information from unstructured text.

For example:

```text
The production API in AWS Mumbai is returning 503 errors.
```

We can extract:

```text
Environment → Production
Service     → API
Cloud       → AWS
Region      → Mumbai
Error       → 503
```

The input is normal human-readable text.

The output is structured information that a program can use.

---

# 3. Why Do We Need a Schema?

We do not want the AI to return random information.

We define exactly what we want:

```text
environment
service
cloud
region
platform
component
error
error_type
start_time
affected_users
severity
issue
trigger
```

This is called a **schema**.

The schema tells the AI:

> These are the fields I want you to extract.

This makes the output predictable and easier for Python to process.

---

# 4. Missing Information

An incident may not contain every entity.

For example:

```text
The frontend service is returning 502 errors.
```

We know:

```text
service → Frontend
error   → 502
```

But we do not know:

```text
cloud
region
platform
severity
affected_users
```

Therefore, we use:

```json
{
  "service": "Frontend",
  "error": "502",
  "cloud": null,
  "region": null,
  "severity": null
}
```

The important rule is:

> Never invent information that is not present in the incident.

---

# 5. Project Setup

Our project contains:

```text
Day-13/
│
├── incident_entity_extractor.py
└── notes.md
```

Activate the virtual environment:

```bash
source ../../venv/Scripts/activate
```

Install the Gemini SDK:

```bash
python -m pip install -U google-genai
```

Verify:

```bash
python -c "from google import genai; print('google-genai works')"
```

Set the API key:

```bash
export GEMINI_API_KEY="your-api-key"
```

We never hardcode the API key inside the Python program.

---

# 6. Import Required Libraries

Our Python program starts with:

```python
import json
import os

from google import genai
```

`os` is used to read the API key from the environment.

`json` is used to validate the AI response.

`genai` is the Gemini SDK.

---

# 7. Create the Gemini Client

We create the client:

```python
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)
```

The API key comes from:

```text
GEMINI_API_KEY
```

This is better than putting the key directly in the source code.

---

# 8. Create the Function

Our application needs a reusable function:

```python
def extract_incident_entities(incident: str) -> str:
    ...
```

The function accepts the incident description.

For example:

```python
incident = """
The production payment API started returning 503 errors
in the AWS Mumbai region at 10:30 AM.
"""
```

The function sends this text to Gemini and returns the extracted JSON.

---

# 9. Build the Prompt

The prompt tells Gemini exactly what to do.

Important instructions include:

```text
Extract the following entities:

environment
service
cloud
region
platform
component
error
error_type
start_time
affected_users
severity
issue
trigger
```

We also tell the model:

```text
Do not invent information.
Use null for missing entities.
Return only valid JSON.
```

These instructions are important because LLMs normally generate natural language.

We need predictable output for our Python application.

---

# 10. Dynamic Prompt

The incident is passed into the prompt using an f-string:

```python
prompt = f"""
Extract incident entities.

Incident:

{incident}
"""
```

This means the function can process different incident descriptions.

We do not need to change the Python code every time.

---

# 11. Send the Request to Gemini

We call:

```python
response = client.models.generate_content(
    model="YOUR_AVAILABLE_GEMINI_MODEL",
    contents=prompt,
)
```

The model receives our prompt and incident description.

Replace:

```text
YOUR_AVAILABLE_GEMINI_MODEL
```

with a Gemini model currently available to your API account.

---

# 12. Get the AI Response

The generated text is available through:

```python
result = response.text.strip()
```

At this point, `result` should contain our JSON.

For example:

```json
{
  "environment": "Production",
  "service": "Payment API",
  "error": "503",
  "severity": "High"
}
```

---

# 13. Validate the JSON

AI output should always be treated as external data.

We validate it using:

```python
json.loads(result)
```

If the response is valid JSON, Python accepts it.

If the response is invalid, Python raises a JSON parsing error.

This is important because downstream applications may depend on the JSON.

---

# 14. Handling Markdown Code Fences

Sometimes an AI model may return:

```text
```json
{
  "service": "Payment API"
}
```
```

Although the content is JSON, the Markdown code fence makes the entire response unsuitable for direct JSON parsing.

We can remove the fences:

```python
if result.startswith("```json"):
    result = result[7:]

if result.startswith("```"):
    result = result[3:]

if result.endswith("```"):
    result = result[:-3]

result = result.strip()
```

Then we validate:

```python
json.loads(result)
```

---

# 15. Complete Program Flow

The application works like this:

```text
Incident Description
        ↓
Python Function
        ↓
Create Prompt
        ↓
Gemini API
        ↓
Extract Entities
        ↓
JSON Response
        ↓
Clean Response
        ↓
Validate JSON
        ↓
Return Result
```

---

# 16. Example

Input:

```text
The production order service running on Kubernetes
started returning HTTP 500 errors at 11:45 AM.
The incident affected approximately 75 customers.
Severity was classified as Critical.
```

The AI should extract information such as:

```json
{
  "environment": "Production",
  "service": "Order Service",
  "platform": "Kubernetes",
  "error": "500",
  "start_time": "11:45 AM",
  "affected_users": 75,
  "severity": "Critical"
}
```

Other fields should be `null` if they are not present.

---

# 17. Why This Is Useful in DevOps

Real incident information can come from:

- Monitoring alerts
- Incident tickets
- Support tickets
- Emails
- Chat messages
- Postmortems
- Application alerts

These sources often contain unstructured text.

Our application can convert that text into structured information.

For example:

```text
Incident Message
       ↓
AI Extractor
       ↓
Service
Environment
Error
Region
Severity
Impact
       ↓
Database / Automation
```

This structured information could later be used for dashboards, incident routing, reporting, or automation.

---

# 18. Important Prompt Engineering Rules

There are four important instructions in this project.

### Define the fields

Tell the AI exactly what to extract.

### Do not invent

Tell the AI to use only information available in the incident.

### Handle missing values

Tell the AI to return `null`.

### Control the format

Tell the AI to return only valid JSON.

Together, these instructions make the output more reliable.

---

# 19. Lab Exercise

Create several different incident descriptions.

For example:

```text
The production authentication service is returning
401 errors on ECS. Approximately 50 users are affected.
The incident started at 2:30 PM and is classified as High.
```

Run the extractor.

Then create another incident with missing information:

```text
The frontend application is slow.
```

Check that the AI does not invent:

```text
AWS
ECS
Region
Users
Severity
```

Instead, missing fields should contain:

```text
null
```

---

# 20. Troubleshooting

### Gemini Import Error

If you see:

```text
ImportError: cannot import name 'genai' from 'google'
```

Run:

```bash
python -m pip install -U google-genai
```

### API Key Problem

Check:

```bash
echo $GEMINI_API_KEY
```

If empty:

```bash
export GEMINI_API_KEY="your-api-key"
```

### Model Not Found

If you receive:

```text
404 NOT_FOUND
```

check that the configured Gemini model is currently available.

---

# 21. Key Takeaways

By the end of this project, you should understand:

- What information extraction is.
- How entity extraction works.
- How to define an extraction schema.
- How to create dynamic prompts.
- How to request structured JSON from Gemini.
- Why missing entities should use `null`.
- Why AI output must be validated.
- How Python can consume structured AI output.
- How AI can be applied to DevOps incident processing.

The core pattern to remember is:

```text
Unstructured Incident
        ↓
        AI
        ↓
Predefined Schema
        ↓
Structured JSON
        ↓
Python Validation
```
---

# Day 14 - AI Knowledge Assistant

## Notes

Building an **AI Knowledge Assistant** using Python and the Gemini API.

The application will receive:

1. A knowledge base
2. A user question

It will then answer the question **only using the provided knowledge base**.

The main idea is:

```text
Knowledge Base
      +
User Question
      ↓
Parameterized Prompt
      ↓
Gemini API
      ↓
Context-Based Answer
      ↓
JSON Validation
```

This is different from a generic chatbot because we are controlling the information that the AI is allowed to use.

---

## 1. What Is a Knowledge Base?

A knowledge base is simply information that we provide to the AI.

For this project, we use a small company IT policy containing:

- Leave Policy
- Password Policy
- VPN Policy
- Working Hours
- IT Support Process
- Laptop and Security Policy

For example:

```text
LEAVE POLICY

Employees are entitled to 18 casual leaves per calendar year.

Leave requests must be submitted through the HR portal.

Sick leave requires manager approval when the sick leave
exceeds 2 consecutive working days.
```

This information becomes the **context** for Gemini.

---

## 2. What Is Context?

Context is the information supplied to the AI before asking the question.

For example:

```text
Context:

Employees are entitled to 18 casual leaves per calendar year.

Question:

How many casual leaves can an employee take?
```

Gemini uses the context to produce the answer.

The important instruction is:

> Answer using only the provided context.

---

## 3. Why Not Build Another Chatbot?

A normal chatbot can answer using the model's general knowledge.

For example:

```text
User Question
      ↓
Gemini
      ↓
General Answer
```

Our application is different:

```text
Knowledge Base
      +
User Question
      ↓
Gemini
      ↓
Answer from Knowledge Base
```

This is called **grounded question answering**.

It is useful when answers must come from specific business information.

Examples include:

- HR policies
- IT documentation
- ERP procedures
- Company SOPs
- Product documentation
- Customer support documentation

---

## 4. Direct Question

Suppose the user asks:

```text
How many casual leaves can an employee take?
```

The knowledge base says:

```text
Employees are entitled to 18 casual leaves per calendar year.
```

Therefore Gemini should answer:

```text
Employees are entitled to 18 casual leaves per calendar year.
```

This is a direct question because the answer is explicitly present in the context.

---

## 5. Interpretation Question

Now consider:

```text
Does one day of sick leave require manager approval?
```

The knowledge base says:

```text
Sick leave requires manager approval when the sick leave
exceeds 2 consecutive working days.
```

The answer is not written exactly as the question.

The model needs to interpret the condition:

```text
Approval required → More than 2 consecutive days

One day → Does not exceed 2 days
```

Therefore:

```text
According to the provided information, manager approval
is not required for one day of sick leave.
```

This teaches us that context-based Q&A can involve simple reasoning over the supplied information.

---

## 6. Missing Information

This is the most important test.

Ask:

```text
What is the company's work-from-home internet reimbursement?
```

Suppose the knowledge base contains no information about internet reimbursement.

The AI must not guess.

Incorrect:

```text
The company provides ₹1,500 per month.
```

There is no information supporting that answer.

Correct:

```text
The provided information does not contain the answer to this question.
```

This is how we begin reducing **AI hallucinations**.

---

## 7. What Is Hallucination?

An AI hallucination occurs when the model generates information that is not supported by the available information.

For example:

```text
Knowledge Base:

Employees receive 18 casual leaves per year.

Question:

What is the company's internet reimbursement?
```

If the AI responds:

```text
Employees receive ₹1,500 per month.
```

that is an unsupported answer.

Our application instead instructs Gemini:

```text
Do not invent information.
If the answer is not available, say so.
```

This does not mathematically guarantee that hallucinations can never happen, so we also validate and test the output.

---

## 8. Structured JSON Output

Instead of asking Gemini for plain text, we ask it to return a fixed JSON structure.

Our schema is:

```json
{
  "answer": null,
  "source": null,
  "found_in_context": false
}
```

The fields have clear meanings.

### `answer`

The answer to the user's question.

### `source`

The policy section containing the relevant information.

### `found_in_context`

Indicates whether the answer was found in the supplied knowledge base.

---

## 9. Successful JSON Response

For:

```text
How many casual leaves can an employee take?
```

the response should look like:

```json
{
  "answer": "Employees are entitled to 18 casual leaves per calendar year.",
  "source": "Leave Policy",
  "found_in_context": true
}
```

The application now knows:

```text
Answer → Available
Source → Leave Policy
Found  → true
```

---

## 10. Missing Answer JSON

For:

```text
What is the company's internet reimbursement?
```

the response should be:

```json
{
  "answer": "The provided information does not contain the answer to this question.",
  "source": null,
  "found_in_context": false
}
```

Notice that:

```text
source = null
found_in_context = false
```

This gives our Python application a clear signal that the information was not available.

---

## 11. Why JSON?

AI normally generates text.

For example:

```text
Employees receive 18 casual leaves per year.
```

A human can understand this easily.

But software applications benefit from structured data.

With JSON:

```json
{
  "answer": "Employees receive 18 casual leaves per year.",
  "source": "Leave Policy",
  "found_in_context": true
}
```

Python can access individual fields:

```python
data["answer"]
data["source"]
data["found_in_context"]
```

This makes the response easier to use in:

- APIs
- Web applications
- Databases
- Automation
- ERP systems
- IT support applications

---

## 12. Prompt Engineering

The prompt is responsible for telling Gemini how to behave.

Important rules include:

```text
Use only the provided knowledge base.

Do not use outside knowledge.

Do not make assumptions.

Do not invent missing information.

If the answer is not available, say so.

Return only valid JSON.

Use the specified JSON structure.
```

These instructions are an example of **prompt engineering**.

The goal is not just to ask a question, but to clearly define the AI's task and constraints.

---

## 13. Parameterized Prompt

Our Python function receives the context and question dynamically:

```python
def answer_question(context: str, question: str) -> str:
```

We then insert them into the prompt:

```python
prompt = f"""
You are an AI Knowledge Assistant.

Use ONLY the provided knowledge base.

Do not use outside knowledge.
Do not make assumptions.
Do not invent missing information.

Knowledge Base:
{context}

Question:
{question}

Return only valid JSON using this structure:

{{
    "answer": null,
    "source": null,
    "found_in_context": false
}}
"""
```

The same function can now handle different questions.

---

## 14. Calling Gemini

We send the prompt to Gemini:

```python
response = client.models.generate_content(
    model="YOUR_AVAILABLE_GEMINI_MODEL",
    contents=prompt,
)
```

The model receives:

```text
Instructions
     +
Knowledge Base
     +
Question
```

and generates the requested response.

The API key is read from the environment:

```python
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)
```

The API key should never be hardcoded.

---

## 15. Reading the Response

Gemini returns text.

We retrieve it using:

```python
result = response.text.strip()
```

The result should contain JSON such as:

```json
{
  "answer": "Employees are entitled to 18 casual leaves per calendar year.",
  "source": "Leave Policy",
  "found_in_context": true
}
```

At this point, it is still a Python string.

---

## 16. JSON Validation

We must validate the AI output before using it.

Use:

```python
json.loads(result)
```

If the JSON is valid:

```text
Gemini Response
      ↓
json.loads()
      ↓
Python Dictionary
```

If it is invalid:

```text
Gemini Response
      ↓
json.loads()
      ↓
JSONDecodeError
```

This is an important software engineering practice.

> Never assume that AI-generated output is automatically valid application data.

---

## 17. Handling Markdown Code Fences

Sometimes a model may return:

```text
```json
{
  "answer": "...",
  "source": "Leave Policy",
  "found_in_context": true
}
```
```

If that happens, remove the Markdown fences before calling `json.loads()`:

```python
if result.startswith("```json"):
    result = result[7:]

if result.startswith("```"):
    result = result[3:]

if result.endswith("```"):
    result = result[:-3]

result = result.strip()
```

Then validate:

```python
json.loads(result)
```

---

## 18. Error Handling

AI applications should handle errors like normal Python applications.

For JSON errors:

```python
try:
    json.loads(result)
except json.JSONDecodeError:
    print("Gemini returned invalid JSON.")
```

For API or runtime errors:

```python
try:
    response = client.models.generate_content(
        model="YOUR_AVAILABLE_GEMINI_MODEL",
        contents=prompt,
    )
except Exception as error:
    print(error)
```

The important lesson is:

> Gemini is one component inside our application. Python still controls validation and error handling.

---

## 19. API Key Security

Do not write:

```python
client = genai.Client(
    api_key="my-secret-key"
)
```

Instead:

```python
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)
```

Set the environment variable:

```bash
export GEMINI_API_KEY="your-api-key"
```

Never commit the API key to GitHub.

---

## 20. Testing the Application

We should test different types of questions.

### Direct Questions

```text
How many casual leaves can employees take?

What is the minimum password length?

When must remote employees use the VPN?

What are the standard working hours?

Where should IT problems be reported?
```

### Interpretation Questions

```text
Does one day of sick leave require manager approval?

Can a remote employee access internal systems without VPN?

What should an employee do after losing their company laptop?
```

### Missing Information

```text
How much internet reimbursement does the company provide?

How many annual vacation days does an employee receive?
```

The last two should demonstrate that the AI does not invent information.

---

## 21. What Should We Verify?

For each question, check four things.

### 1. Answer

Is the answer supported by the knowledge base?

### 2. Source

Does the source identify the correct policy?

### 3. Found Status

For available information:

```json
"found_in_context": true
```

For unavailable information:

```json
"found_in_context": false
```

### 4. JSON

Does this work successfully?

```python
json.loads(result)
```

Also check that the model did not introduce information that is absent from the knowledge base.

---

## 22. Complete Application Flow

The complete flow is:

```text
Company IT Knowledge Base
          ↓
      User Question
          ↓
   Python Application
          ↓
   Parameterized Prompt
          ↓
      Gemini API
          ↓
 Context-Based Reasoning
          ↓
     JSON Response
          ↓
     json.loads()
          ↓
   Validated JSON
          ↓
 Answer + Source + Status
```

---

## 23. Key Concepts Learned

### Context

Information supplied to the AI along with the question.

### Grounding

Keeping the AI answer connected to trusted information.

### Prompt Engineering

Writing instructions that control how the model should perform the task.

### Structured Output

Requesting predictable JSON instead of unrestricted text.

### JSON Validation

Using Python to verify that the generated response is valid JSON.

### Hallucination Reduction

Preventing the AI from inventing information that does not exist in the supplied context.

### Knowledge-Based Q&A

Answering questions from a provided knowledge base instead of relying only on the model's general knowledge.

---

## 24. Final Takeaway

The main concept of Day 14 is:

```text
Knowledge Base
      +
Question
      ↓
Gemini
      ↓
Grounded Answer
```

The most important rule is:

```text
If the information exists:
    Answer from the context.

If the information does not exist:
    Do not invent it.
```
---

# 📚 Day 15 — AI Document Analyzer

## 1. What Are We Building?

Today we are building an **AI Document Analyzer**.

The application takes an unstructured document such as:

- ERP process
- SOP
- Technical specification
- Project requirements
- Incident runbook

and asks Gemini to extract useful information into structured JSON.

The basic idea is:

    Document
       ↓
    Gemini
       ↓
    Structured Information
       ↓
    JSON

This is different from a normal summarizer.

A summarizer answers:

    "What is this document about?"

Our application answers:

    "What requirements, roles, actions, rules, dependencies,
     exceptions, and risks are present in this document?"

---

# 2. Why Is This Useful?

Business documents usually contain important information in natural language.

For example:

    Requests above $10,000 require approval from the finance department.

A human can understand this easily.

But an application needs structured information:

    {
      "rule": "Requests above $10,000 require finance approval"
    }

Once information is structured, it can be used by:

- APIs
- Databases
- ERP systems
- Workflow automation
- Dashboards
- Reporting systems
- Other AI applications

This is one of the important patterns in enterprise AI:

    Unstructured Data
          ↓
          AI
          ↓
    Structured Data

---

# 3. Flow

The flow is:

    Business Document
          ↓
    Gemini
          ↓
    Document Analysis
          ↓
    Structured JSON

We are asking the AI to analyze the complete document.

---

# 4. What Information Are We Extracting?

Our JSON contains eight main categories.

## Document Type

Identifies what kind of document was provided.

Example:

    "document_type": "ERP Purchase Process"

---

## Requirements

Requirements describe things that must be provided or satisfied.

Example:

    "Purchase requests must contain an estimated price."

Requirements are useful when analyzing:

- Software requirements
- Policies
- SOPs
- Technical specifications

---

## Roles

Roles identify people, teams, or departments involved.

Example:

    Employee
    Manager
    Procurement Team
    Finance Department

This helps us understand **who is responsible for what**.

---

## Actions

Actions describe activities that must be performed.

Example:

    Create a purchase request.
    Approve the request.
    Create a purchase order.
    Record a goods receipt.

Actions are especially useful for workflow automation.

---

## Dependencies

A dependency describes something that must happen before another action.

Example:

    Purchase order creation depends on approval.

The process is:

    Purchase Request
          ↓
    Approval
          ↓
    Purchase Order

Therefore, the purchase order depends on approval.

---

## Rules

Rules describe conditions, restrictions, thresholds, or mandatory behavior.

Example:

    Requests above $10,000 require finance approval.

Another example:

    Payment must not be released if invoice matching fails.

---

## Exceptions

Exceptions describe situations where the normal process changes.

Example:

    Urgent purchases may bypass the normal process
    with proper authorization.

Normal process:

    Request
      ↓
    Approval
      ↓
    Purchase Order

Exception:

    Urgent Purchase
          ↓
    Authorized Bypass

---

## Risks

Risks describe possible problems or consequences explicitly mentioned in the document.

Example:

    Missing approvals can create unauthorized purchases.

Another example:

    Invoice matching failures can result in payment errors.

The AI should extract risks from the document rather than inventing possible risks.

---

# 5. The JSON Schema

Our fixed output structure is:

    {
      "document_type": "",
      "requirements": [],
      "roles": [],
      "actions": [],
      "dependencies": [],
      "rules": [],
      "exceptions": [],
      "risks": []
    }

Why use a fixed structure?

Because applications need predictable data.

For example:

    data["roles"]

will always refer to the roles extracted from the document.

If the document contains no exceptions, we return:

    "exceptions": []

rather than inventing an exception.

---

# 6. The Most Important AI Rule

The analyzer must use:

**ONLY the information contained in the supplied document.**

The model must not:

- Use outside knowledge
- Guess missing information
- Invent business rules
- Invent responsibilities
- Invent risks
- Add unsupported facts

For example, if the document says:

    Employees must submit purchase requests through the ERP.

But does not mention:

    How long approval takes

The AI must not invent:

    "Approval takes 2 business days."

Instead:

    "dependencies": []

or another appropriate category should simply omit unsupported information.

---

# 7. Parameterized Prompt

The document is inserted into the prompt dynamically.

Conceptually:

    prompt = f"""
    Analyze this document.

    DOCUMENT:
    {document}
    """

This is called a **parameterized prompt**.

The Python program can therefore analyze different documents without changing the prompt logic.

For example:

    purchase_process.txt

can later become:

    software_requirements.txt

or:

    incident_runbook.txt

The analyzer stays the same.

---

# 8. Reading the Document

Python reads the document using:

    with open(
        "purchase_process.txt",
        "r",
        encoding="utf-8"
    ) as file:

        document = file.read()

Now:

    document

contains the complete text.

We then pass it to:

    analyze_document(document)

This separates two responsibilities:

    File Reading
         ↓
    AI Analysis

This separation is important because later we can replace the file reader with:

- PDF extraction
- DOCX extraction
- Database content
- API content
- Uploaded files

without changing the core AI analyzer.

---

# 9. Gemini API

We use the `google-genai` Python SDK.

The application creates a client using:

    GEMINI_API_KEY

The API key should come from an environment variable.

Never write:

    api_key = "my-secret-key"

inside the Python source code.

Instead use:

    GEMINI_API_KEY

This prevents accidentally committing credentials to GitHub.

---

# 10. Why Use `.env`?

We can store the key in:

    .env

Example:

    GEMINI_API_KEY=your-api-key

Python can load it using:

    from dotenv import load_dotenv

    load_dotenv()

Then:

    os.environ.get("GEMINI_API_KEY")

reads the key.

The `.env` file should be included in:

    .gitignore

---

# 11. AI Output Is Not Automatically Trustworthy

One important lesson today is:

**AI output must be validated before application code uses it.**

Gemini might return valid JSON:

    {
      "document_type": "ERP Purchase Process"
    }

But it could also accidentally return:

    Here is the analysis:

    ```json
    {
      ...
    }
    ```

That is not directly usable as JSON because of the Markdown wrapper.

The application can remove accidental code fences and then validate the result.

---

# 12. JSON Validation

Python provides:

    json.loads()

Example:

    data = json.loads(result)

If the response is valid JSON:

    Gemini Response
          ↓
    json.loads()
          ↓
    Python Dictionary

If it is invalid:

    Gemini Response
          ↓
    json.loads()
          ↓
    JSONDecodeError

This allows the application to detect invalid AI output.

---

# 13. Validate the Schema Too

Valid JSON does not necessarily mean correct application data.

For example, this is valid JSON:

    {
      "hello": "world"
    }

But it does not follow our analyzer schema.

Therefore we should check that these fields exist:

    document_type
    requirements
    roles
    actions
    dependencies
    rules
    exceptions
    risks

This gives us two levels of validation:

    JSON Syntax Validation
              ↓
    Schema / Field Validation

---

# 14. Example ERP Document

Our lab uses an ERP purchase process.

The process is:

    Purchase Request
          ↓
    Manager Approval
          ↓
    Purchase Order
          ↓
    Goods Receipt
          ↓
    Invoice Verification

The AI should understand that these are related process steps.

For example:

    Purchase Order
    depends on
    Manager Approval

And:

    Invoice Verification
    depends on
    Purchase Order + Goods Receipt

This demonstrates why document analysis is more useful than simple summarization.

---

# 15. Important Business Rules

From our ERP document, examples include:

    Requests above $10,000 require additional approval.

    Purchase orders must not be created before
    required approvals.

    Payment must not be released when invoice
    matching fails.

These should be extracted under:

    "rules"

The AI should preserve important conditions such as:

    $10,000

It should not change the meaning.

---

# 16. Important Exceptions

The ERP document contains an exception:

    Urgent purchases may bypass the normal process
    with authorization.

This belongs under:

    "exceptions"

An exception is different from a normal rule.

A rule says:

    What normally must happen.

An exception says:

    When the normal process can change.

---

# 17. Important Risks

The document explicitly mentions risks such as:

    Missing approvals can create unauthorized purchases.

    Incorrect goods receipts can result in incorrect
    supplier payments.

    Invoice matching failures can result in payment
    errors or fraud.

These belong under:

    "risks"

The key point is that the AI extracts documented risks.

It should not create unrelated risks based on general knowledge.

---

# 18. Why Structured JSON Matters

Imagine the AI returned:

    The ERP process starts with a purchase request,
    followed by approval and purchase order creation...

A human can read it.

But an application has difficulty reliably extracting individual items.

Structured JSON gives us:

    {
      "roles": [
        "Employee",
        "Manager",
        "Procurement Team"
      ],
      "actions": [
        "Create purchase request",
        "Approve purchase request",
        "Create purchase order"
      ]
    }

Python can now process these values directly.

For example:

    data["roles"]

or:

    data["actions"]

This makes the AI response application-friendly.

---

# 19. Reusable Analyzer

One of the most important design ideas is that the analyzer should not be tied to one document.

Today:

    purchase_process.txt
          ↓
    analyze_document()

Tomorrow:

    software_requirements.txt
          ↓
    analyze_document()

Another day:

    incident_runbook.txt
          ↓
    analyze_document()

The AI analysis function remains the same.

Only the input document changes.

This is what makes the application reusable.

---

# 20. Testing

Test the application with at least two different documents.

### Test 1 — ERP Purchase Process

Check whether the AI identifies:

- Employees
- Managers
- Procurement
- Finance
- Purchase actions
- Approval dependencies
- Approval rules
- Urgent purchase exception
- Business risks

### Test 2 — Software Requirements

Use requirements such as:

    Users must be able to register.

    Users must be able to log in.

    The account must be locked after five failed attempts.

    Administrators can unlock accounts.

    The system must respond within two seconds.

Check whether the analyzer extracts these correctly.

---

# 21. Common Mistakes

## Hardcoding the document

Avoid putting the entire document inside the Python function.

Instead:

    document = file.read()

    analyze_document(document)

---

## Hardcoding the API key

Never do:

    genai.Client(api_key="secret")

Use:

    GEMINI_API_KEY

---

## Trusting AI output blindly

Do not directly assume:

    response.text

is valid JSON.

Always validate it.

---

## Allowing hallucination

The prompt should clearly say:

    Use ONLY the provided document.

---

## Returning inconsistent fields

Always return the same schema:

    document_type
    requirements
    roles
    actions
    dependencies
    rules
    exceptions
    risks

---

# 22. Day 15 Architecture

The complete architecture is:

    ┌──────────────────────┐
    │ Business Document    │
    │ .txt / .md           │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │ Python File Reader   │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │ Parameterized Prompt │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │ Gemini API           │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │ Structured JSON      │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │ json.loads()         │
    │ Validation            │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │ JSON File / App      │
    └──────────────────────┘

---

# 23. Key Terms

### Document Intelligence

Using AI to understand and extract information from documents.

### Structured Data

Data organized into predictable fields such as JSON.

### Unstructured Data

Natural-language information such as documents, policies, and reports.

### Prompt Grounding

Restricting the AI to information supplied in the prompt.

### JSON Validation

Checking whether the AI response is valid JSON before using it.

### Information Extraction

Finding specific useful information inside unstructured text.

### Parameterized Prompt

A prompt where application data is inserted dynamically.

---

# 24. What We Learned Today

The main lessons from Day 15 are:

1. AI can analyze complete business documents.
2. Natural language can be converted into structured JSON.
3. A fixed schema makes AI output easier to consume.
4. AI should be grounded in the supplied document.
5. AI output must be validated before application use.
6. Documents should be loaded dynamically.
7. The analyzer should be reusable across different documents.
8. Structured extraction is useful for enterprise automation.

---

# 📚 Day 16 — AI Text Embeddings Notes

## 1. What Are Text Embeddings?

A text embedding is a numerical representation of text that captures aspects of its meaning.

Instead of representing a sentence only as characters or words, an embedding model converts it into a vector of numbers.

Example:

```text
"I love working with Python."
            ↓
      Embedding Model
            ↓
[0.023, -0.184, 0.421, ...]
```

The individual numbers are not normally interpreted one by one.

The important idea is that sentences with related meanings tend to have vectors that are closer together in the embedding space.

```text
Similar meaning
      ↓
Similar vectors
      ↓
Higher similarity
```

---

## 2. Why Are Embeddings Useful?

Embeddings allow text to be compared mathematically based on meaning rather than exact word matching.

For example:

```text
"Python is a programming language."

"I enjoy writing Python applications."
```

These sentences use different words but discuss related concepts.

An embedding model can represent their meanings as vectors and allow their similarity to be calculated.

Common applications include:

- Semantic search
- Recommendation systems
- Document retrieval
- Similarity matching
- Vector databases
- RAG systems
- AI knowledge bases
- Duplicate or related-content detection

---

## 3. Embedding Model

An embedding model takes text as input and produces a vector as output.

The basic process is:

```text
Text
 ↓
Embedding Model
 ↓
Numerical Vector
```

For this project, the model is:

```text
all-MiniLM-L6-v2
```

It is available through the `sentence-transformers` Python library.

The model produces a fixed-size embedding for each input sentence.

For this model, the embedding contains:

```text
384 dimensions
```

Therefore, one sentence becomes a vector containing 384 numerical values.

---

## 4. Vector Representation

Consider:

```text
Python is a programming language.
```

The embedding model converts it into something conceptually like:

```text
[0.0123, -0.0842, 0.0317, 0.0921, ...]
```

The complete vector represents the sentence in a high-dimensional mathematical space.

The values do not have simple meanings such as:

```text
Dimension 1 = Python
Dimension 2 = programming
```

Instead, the information is distributed across the vector.

Therefore, the complete vector should be considered as the representation.

---

## 5. Embedding Dimensions

A dimension is one numerical position in an embedding vector.

For `all-MiniLM-L6-v2`:

```text
1 sentence
    ↓
384 numerical values
    ↓
384-dimensional vector
```

The number of dimensions is determined by the embedding model.

Different embedding models can produce vectors with different dimensions.

---

## 6. Sentence Transformers

`sentence-transformers` is a Python library designed for generating useful embeddings for sentences and other text.

Installation:

```bash
python -m pip install sentence-transformers
```

Import:

```python
from sentence_transformers import SentenceTransformer
```

Load the model:

```python
model = SentenceTransformer("all-MiniLM-L6-v2")
```

Generate an embedding:

```python
embedding = model.encode(
    "Python is a programming language."
)
```

The result is a numerical vector.

---

## 7. Generating Multiple Embeddings

Multiple sentences can be encoded together.

Example:

```python
sentences = [
    "Python is a programming language.",
    "I enjoy writing Python applications.",
    "I like eating pizza."
]

embeddings = model.encode(
    sentences,
    convert_to_numpy=True
)
```

The result contains one embedding vector for each sentence.

Conceptually:

```text
Sentence 1 → Vector 1
Sentence 2 → Vector 2
Sentence 3 → Vector 3
```

---

## 8. NumPy

NumPy is used for numerical operations on vectors and arrays.

Installation:

```bash
python -m pip install numpy
```

Import:

```python
import numpy as np
```

NumPy provides operations required for similarity calculations, including:

- Dot product
- Vector magnitude
- Array operations
- Numerical calculations

---

## 9. Similarity Between Vectors

After converting sentences into embeddings, the vectors can be compared.

Example:

```text
Sentence A
    ↓
Vector A

Sentence B
    ↓
Vector B

Vector A + Vector B
        ↓
Similarity calculation
        ↓
Similarity score
```

A commonly used method for text embeddings is **cosine similarity**.

---

# 10. Cosine Similarity

Cosine similarity measures the angle between two vectors.

The basic formula is:

```text
cosine similarity =
(A · B)
───────────────
||A|| × ||B||
```

Where:

- `A · B` is the dot product
- `||A||` is the magnitude of vector A
- `||B||` is the magnitude of vector B

The calculation focuses on the direction of the vectors.

Conceptually:

```text
Similar direction
       ↘
        ↘
         ↘
```

means the vectors are more similar.

---

## 11. Cosine Similarity in Python

A simple implementation:

```python
def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)

    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )
```

The important NumPy operations are:

```python
np.dot()
```

Calculates the dot product.

```python
np.linalg.norm()
```

Calculates the magnitude of a vector.

---

## 12. Understanding Similarity Scores

Cosine similarity is often used to determine how closely two vectors point in the same direction.

For many normalized embedding use cases, scores can be interpreted approximately as:

```text
Higher similarity
       ↓
More semantically related

Lower similarity
       ↓
Less semantically related
```

Exact score interpretation depends on the embedding model and the type of text.

A score should therefore be interpreted in context rather than treated as a universal threshold.

---

## 13. Example Comparison

Consider:

```text
Sentence A:
Python is a programming language.

Sentence B:
I enjoy writing Python applications.
```

Both sentences are related to Python and programming.

Their embeddings should generally have relatively high similarity.

Now compare:

```text
Sentence A:
Python is a programming language.

Sentence C:
I like eating pizza.
```

These sentences discuss different topics.

Their similarity should generally be lower.

The important concept is:

```text
Related meaning
      ↓
Closer vectors
      ↓
Higher similarity
```

---

# 14. Semantic Search

Semantic search finds information based on meaning rather than simply matching keywords.

Suppose the stored sentences are:

```text
Python is a programming language.
I enjoy writing Python applications.
AWS provides cloud computing services.
Cloud infrastructure can be deployed on AWS.
I like eating pizza.
```

The query is:

```text
I want to learn Python programming.
```

The query is converted into an embedding.

Then the query embedding is compared with every stored sentence embedding.

```text
Query
 ↓
Query Embedding
 ↓
Compare with stored vectors
 ↓
Calculate similarity scores
 ↓
Sort by similarity
 ↓
Return closest sentence
```

---

## 15. Semantic Search Example

Conceptually:

```text
Query:
"I want to learn Python programming."
                ↓
          Query Vector
                ↓
       ┌────────┼────────┐
       ↓        ↓        ↓
    Vector 1  Vector 2  Vector 3
       ↓        ↓        ↓
     Score    Score    Score
       └────────┼────────┘
                ↓
        Highest similarity
                ↓
        Most similar sentence
```

The search is based on the relationship between embeddings.

The query does not have to exactly match the words in the stored sentence.

---

# 16. Reading Sentences from a File

Keeping the sentences in a separate file makes the application reusable.

Example:

```python
def load_sentences(filename):
    with open(filename, "r", encoding="utf-8") as file:
        sentences = [
            line.strip()
            for line in file
            if line.strip()
        ]

    return sentences
```

Then:

```python
sentences = load_sentences("sentences.txt")
```

Each non-empty line becomes one sentence.

---

# 17. Complete Embedding Flow

The complete application follows this process:

```text
sentences.txt
      ↓
Read sentences
      ↓
Load embedding model
      ↓
Generate embeddings
      ↓
Store vectors
      ↓
Compare vectors
      ↓
Calculate cosine similarity
      ↓
Perform semantic search
      ↓
Save results
```

---

# 18. Why Embeddings Are Different from Generated Text

An embedding model does not normally produce a natural-language answer.

Input:

```text
Python is a programming language.
```

Output:

```text
[0.0123, -0.0842, 0.0317, ...]
```

The output is a numerical representation.

Therefore:

```text
Generative AI
    ↓
Generates text

Embedding model
    ↓
Generates vectors
```

Embeddings are primarily useful for comparing, retrieving, organizing, and searching information.

---

# 19. Vector Database Concept

When only a few sentences are stored, vectors can remain in memory.

For a large application, embeddings can be stored in a vector database.

Conceptually:

```text
Documents
    ↓
Embedding Model
    ↓
Vectors
    ↓
Vector Database
```

When a user searches:

```text
User Query
    ↓
Query Embedding
    ↓
Vector Search
    ↓
Relevant Documents
```

This allows large collections of information to be searched semantically.

---

# 20. Connection to RAG

Embeddings are an important component of Retrieval-Augmented Generation (RAG).

A simplified RAG architecture is:

```text
Documents
    ↓
Create embeddings
    ↓
Store vectors
    ↓
       Vector Database
              ↑
              │
User Question
      ↓
Question Embedding
      ↓
Similarity Search
      ↓
Relevant Documents
      ↓
LLM
      ↓
Generated Answer
```

The embedding system helps retrieve relevant information.

The language model can then use the retrieved information to generate an answer.

---

# 21. Important Concepts

### Embedding

A numerical representation of text.

### Vector

An ordered collection of numerical values.

Example:

```text
[0.12, -0.08, 0.31, ...]
```

### Dimension

One numerical position in a vector.

### Embedding Model

A model that converts text into embeddings.

### Cosine Similarity

A mathematical method for comparing the direction of two vectors.

### Semantic Similarity

Similarity based on meaning rather than exact word matching.

### Semantic Search

Search that retrieves information based on meaning.

### Vector Database

A database designed to store and search vector representations efficiently.

---

# 22. Key Python Components

Load the model:

```python
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
```

Generate embeddings:

```python
embeddings = model.encode(
    sentences,
    convert_to_numpy=True
)
```

Calculate dot product:

```python
np.dot(vector_a, vector_b)
```

Calculate vector magnitude:

```python
np.linalg.norm(vector_a)
```

Calculate similarity:

```python
similarity = cosine_similarity(
    vector_a,
    vector_b
)
```

Sort search results:

```python
results.sort(
    key=lambda item: item["similarity"],
    reverse=True
)
```

---

# 23. Practical Mental Model

The easiest way to understand embeddings is:

```text
Text
 ↓
Meaning representation
 ↓
Numbers
 ↓
Vector
 ↓
Compare vectors
 ↓
Measure semantic similarity
```

The vector itself is not the final answer.

It is a mathematical representation that makes operations such as similarity search possible.

---

# 24. Common Applications

Embeddings can be used for:

- Searching documents by meaning
- Finding similar documents
- Finding similar questions
- Recommendation systems
- FAQ matching
- Duplicate detection
- Clustering related content
- Document retrieval
- RAG
- Knowledge-base search
- Matching users with relevant content

---

# 25. Key Takeaways

- Text can be converted into numerical vectors called embeddings.
- An embedding represents information about the meaning of text.
- The complete vector is more important than any individual number.
- Different embedding models can produce different vector sizes.
- `sentence-transformers` provides convenient tools for generating sentence embeddings.
- `all-MiniLM-L6-v2` produces 384-dimensional sentence embeddings.
- NumPy provides the numerical operations required for vector calculations.
- Cosine similarity can be used to compare embedding vectors.
- Semantically related sentences generally have higher similarity than unrelated sentences.
- Semantic search uses embeddings to find information based on meaning.
- Embeddings are a fundamental building block for vector databases and RAG systems.

---

# 🎯 Core Idea

```text
             TEXT
               │
               ▼
       EMBEDDING MODEL
               │
               ▼
            VECTOR
               │
               ▼
      VECTOR COMPARISON
               │
               ▼
     SEMANTIC SIMILARITY
               │
               ▼
       SEARCH / RETRIEVAL
```

**Text → Vector → Similarity → Meaning-based Retrieval**

This is the fundamental idea behind AI text embeddings.

---


# 🚀 Day 17 — AI Semantic Search 🔎

## 1. What Is Semantic Search?

Semantic search is a search technique that finds information based on **meaning**, rather than only matching exact keywords.

Traditional keyword search might process:

    Query:
    How can I automate AWS infrastructure?

and look for words such as:

    AWS
    automate
    infrastructure

Semantic search works differently:

```text
User Query
    ↓
Embedding Model
    ↓
Query Vector
    ↓
Compare with Document Vectors
    ↓
Cosine Similarity
    ↓
Rank Results
    ↓
Top Matching Documents
```

The important idea is:

```text
Search by meaning
       ↓
Not only by exact words
```

A query does not necessarily need to contain the exact name of the technology mentioned in the relevant document.

For example:

```text
Query:
How can I automate infrastructure?

Document:
Terraform allows infrastructure to be defined as code.
```

The query does not contain the word `Terraform`, but the two texts are semantically related.

---

# 2. Why Semantic Search Is Useful

Keyword search can fail when two pieces of text express the same idea using different words.

Example:

```text
Query:
How can I run applications in containers?
```

A relevant document might say:

```text
Docker packages applications into portable containers.
```

The wording is not identical, but the meaning is closely related.

Semantic search is useful for:

- Knowledge bases
- Documentation search
- Customer support
- Enterprise search
- Recommendation systems
- Document retrieval
- Question answering
- RAG applications

---

# 3. What Is an Embedding?

An embedding is a numerical representation of text.

A sentence is passed into an embedding model:

```text
Text
 ↓
Embedding Model
 ↓
Numerical Vector
```

For example:

```text
"Terraform manages infrastructure."
            ↓
      Embedding Model
            ↓
[0.12, -0.43, 0.27, ...]
```

The vector contains many numerical dimensions.

The individual numbers are generally not meaningful to a human.

The important property is the relationship between vectors.

Conceptually:

```text
Similar meaning
      ↓
Nearby / similar representations

Different meaning
      ↓
Less similar representations
```

This allows mathematical techniques to compare pieces of text.

---

# 4. Sentence Transformers

The project uses the `sentence-transformers` Python library.

A Sentence Transformer provides models that can convert sentences and other text into embeddings suitable for similarity comparison.

The model used in this project is:

```text
all-MiniLM-L6-v2
```

The basic process is:

```text
Sentence
   ↓
all-MiniLM-L6-v2
   ↓
Embedding Vector
```

The same model must be used for both:

- Stored documents
- User queries

This allows their embeddings to exist in the same vector space and be compared meaningfully.

---

# 5. The Semantic Search Pipeline

The complete pipeline is:

```text
Documents
    ↓
Generate Embeddings
    ↓
Store Document Vectors
    ↓
User Query
    ↓
Generate Query Embedding
    ↓
Compare Query Vector
with Document Vectors
    ↓
Cosine Similarity
    ↓
Sort by Similarity
    ↓
Top-K Results
```

In this project:

```text
K = 3
```

Therefore, the application returns the three highest-scoring documents.

---

# 6. Knowledge Collection

A semantic search system needs information to search.

For the project, the collection contains Cloud and DevOps knowledge such as:

```text
AWS EC2 provides resizable compute capacity.

Amazon S3 is an object storage service.

Docker packages applications into portable containers.

Kubernetes orchestrates containerized applications.

Terraform allows infrastructure to be defined as code.

GitLab CI/CD automates software build and deployment pipelines.

AWS Lambda runs code without managing servers.

Amazon RDS provides managed relational databases.

AWS VPC provides networking capabilities for cloud resources.

Prometheus collects metrics and monitors applications and infrastructure.

Grafana provides dashboards for monitoring metrics and system performance.

Ansible automates configuration management and application deployment.

Jenkins automates continuous integration and continuous delivery.

Amazon CloudWatch monitors AWS resources and applications.

Docker Compose defines and runs multi-container applications.
```

Each sentence is treated as a separate document.

---

# 7. Document Embeddings

Before searching, every document is converted into an embedding.

For example:

```text
Terraform allows infrastructure to be defined as code.
                         ↓
                 Embedding Model
                         ↓
                  Document Vector
```

This happens for every document.

Conceptually:

```text
Document 1 → Vector 1
Document 2 → Vector 2
Document 3 → Vector 3
Document 4 → Vector 4
...
Document 15 → Vector 15
```

These vectors are kept in memory for the search operation.

---

# 8. Query Embedding

When a user enters a query such as:

```text
How can I automate infrastructure?
```

the query is also converted into an embedding:

```text
User Query
    ↓
Embedding Model
    ↓
Query Vector
```

The query vector is then compared with every stored document vector.

---

# 9. Cosine Similarity

Cosine similarity measures how similar two vectors are based on their direction.

The formula is:

```text
cosine similarity =
    (A · B)
    ─────────────
    ||A|| × ||B||
```

Where:

- `A` is the first vector
- `B` is the second vector
- `A · B` is the dot product
- `||A||` is the magnitude of vector A
- `||B||` is the magnitude of vector B

The important concept is not memorizing the formula, but understanding the purpose:

```text
Two embeddings
      ↓
Compare their directions
      ↓
Produce similarity score
```

For this project, a higher score generally means greater semantic similarity.

---

# 10. Why Vector Direction Matters

Imagine two vectors:

```text
Vector A ────────→
Vector B ────────→
```

If they point in similar directions, their cosine similarity is high.

If they point in very different directions, the similarity is lower.

This gives a mathematical way to compare semantic representations.

The exact score should not be treated as a universal measure of how similar two sentences are.

Scores depend on:

- Embedding model
- Query
- Document
- Domain
- Text length
- Model version

The most useful operation here is **ranking**.

---

# 11. Ranking Documents

Suppose a query is compared with five documents:

```text
Document A → 0.87
Document B → 0.81
Document C → 0.74
Document D → 0.42
Document E → 0.29
```

After sorting:

```text
1. Document A → 0.87
2. Document B → 0.81
3. Document C → 0.74
4. Document D → 0.42
5. Document E → 0.29
```

If `TOP_K = 3`, only these are returned:

```text
1. Document A
2. Document B
3. Document C
```

This is called **Top-K retrieval**.

---

# 12. Example Search

Query:

```text
How can I automate infrastructure?
```

Possible relevant results:

```text
1. Terraform allows infrastructure to be defined as code.

2. Ansible automates configuration management and application deployment.

3. GitLab CI/CD automates software build and deployment pipelines.
```

The exact similarity scores and ordering depend on the embedding model and input text.

The important result is that the system retrieves documents related to the meaning of the query.

---

# 13. Another Example

Query:

```text
Which AWS service provides object storage?
```

A highly relevant result is:

```text
Amazon S3 is an object storage service.
```

The system does not need to perform a complicated rule such as:

```text
AWS + object + storage
```

Instead:

```text
Query
 ↓
Embedding
 ↓
Similarity Search
 ↓
S3 Document
```

---

# 14. Container Search Example

Query:

```text
How can applications be run in containers?
```

Relevant results can include:

```text
Docker packages applications into portable containers.

Kubernetes orchestrates containerized applications.

Docker Compose defines and runs multi-container applications.
```

The results are obtained by comparing semantic representations.

---

# 15. Managed Database Search

Query:

```text
What can be used for managed relational databases?
```

Relevant result:

```text
Amazon RDS provides managed relational databases.
```

Again, the purpose is not exact phrase matching.

The embedding model helps represent the relationship between the concepts.

---

# 16. Important Difference Between Documents and Queries

Documents are embedded before or during indexing.

The query is embedded when the user searches.

Conceptually:

```text
             DOCUMENT SIDE

Documents
   ↓
Embedding Model
   ↓
Document Embeddings
   ↓
Stored for Search

              QUERY SIDE

User Query
   ↓
Embedding Model
   ↓
Query Embedding
   ↓
Similarity Search
```

Both sides use the same embedding model.

---

# 17. NumPy's Role

NumPy is used for numerical operations on vectors.

For example:

```python
np.dot(vector_a, vector_b)
```

calculates the dot product.

And:

```python
np.linalg.norm(vector_a)
```

calculates the magnitude of a vector.

These operations are used to calculate cosine similarity.

Therefore:

```text
Sentence Transformers
        ↓
Creates vectors

NumPy
        ↓
Performs vector mathematics
```

---

# 18. The Core Search Function

The semantic search function performs several steps.

```text
Query
 ↓
Encode query
 ↓
Calculate similarity with every document
 ↓
Create result list
 ↓
Sort results
 ↓
Return Top-K
```

Conceptually:

```python
query_embedding = model.encode(query)

for document_embedding in document_embeddings:
    similarity = cosine_similarity(
        query_embedding,
        document_embedding
    )

results.sort(
    key=lambda result: result["similarity"],
    reverse=True
)
```

The `reverse=True` argument ensures the highest similarity appears first.

---

# 19. Why `encode()` Is Important

The Sentence Transformer model provides the `encode()` method.

For documents:

```python
document_embeddings = model.encode(
    documents,
    convert_to_numpy=True
)
```

For a query:

```python
query_embedding = model.encode(
    query,
    convert_to_numpy=True
)
```

Therefore:

```text
encode(document)
       ↓
document vector

encode(query)
       ↓
query vector
```

`convert_to_numpy=True` makes the result available as NumPy arrays, which are convenient for mathematical operations.

---

# 20. Interactive Search

The application uses an interactive loop.

Conceptually:

```text
Start Application
       ↓
Load Model
       ↓
Create Document Embeddings
       ↓
Wait for Query
       ↓
Search
       ↓
Display Top 3
       ↓
Wait for Another Query
       ↓
Exit?
  ↓       ↓
 Yes      No
  ↓       ↓
Stop     Search Again
```

The user can enter multiple queries without restarting the program.

Entering:

```text
exit
```

stops the application.

---

# 21. Why the Model Is Loaded Once

Loading the embedding model can take time.

Therefore, the model should be loaded once when the application starts:

```python
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
```

It should not be loaded again for every query.

The better flow is:

```text
Application Starts
       ↓
Load Model Once
       ↓
Create Document Embeddings
       ↓
Process Many Queries
```

This makes repeated searches much more efficient.

---

# 22. Why Document Embeddings Are Created Once

The documents do not change during a normal search session.

Therefore, their embeddings can be generated once:

```text
Documents
   ↓
Embeddings
   ↓
Keep in Memory
```

For every new query, only the query needs to be embedded again.

```text
New Query
   ↓
Query Embedding
   ↓
Compare with Existing Document Embeddings
```

This avoids unnecessary computation.

---

# 23. In-Memory Retrieval

The Day 17 application keeps the vectors in memory.

For a small collection:

```text
15 Documents
    ↓
15 Embeddings
    ↓
Stored in Python memory
```

This is simple and useful for learning.

For large systems, storing and searching thousands or millions of vectors requires specialized vector search infrastructure.

That is where technologies such as vector databases and approximate nearest-neighbor indexes become useful.

---

# 24. Top-K Retrieval

`TOP_K` controls the number of results returned.

Example:

```python
TOP_K = 3
```

If there are 15 documents:

```text
15 Documents
     ↓
Similarity Calculation
     ↓
Sort
     ↓
Top 3
```

This prevents the application from displaying every document when only the most relevant results are needed.

---

# 25. Similarity Is Not the Same as Truth

A high similarity score does not mean that a document is factually correct.

It only means that the document's embedding is close to the query embedding according to the model.

For example:

```text
High similarity
       ≠
Guaranteed factual accuracy
```

Semantic search is a retrieval mechanism, not a fact-checking mechanism.

---

# 26. Limitations of This Simple Search Engine

The Day 17 implementation is intentionally small.

It has some limitations:

- Documents are stored directly in Python.
- Embeddings are stored only in memory.
- Every query compares against every document.
- There is no persistent vector database.
- There is no metadata filtering.
- There is no document chunking.
- There is no keyword + semantic hybrid search.
- There is no LLM-generated answer.

These are appropriate improvements for more advanced retrieval systems.

---

# 27. What Happens With More Documents?

Suppose there are:

```text
15 documents
```

A simple search can compare the query against all 15.

With:

```text
1,000 documents
```

it compares against 1,000 vectors.

With:

```text
1,000,000 documents
```

comparing against every vector for every query becomes increasingly expensive.

Large-scale systems therefore use optimized vector indexes and vector databases.

Examples include:

- FAISS
- Chroma
- Qdrant
- Weaviate
- Pinecone

The Day 17 project does not require these technologies.

The focus is understanding the basic retrieval mechanism first.

---

# 28. Semantic Search and RAG

Semantic search is a fundamental component of Retrieval-Augmented Generation, commonly called **RAG**.

A simple semantic search system:

```text
Documents
    ↓
Embeddings
    ↓
Query
    ↓
Similarity Search
    ↓
Relevant Documents
```

A RAG system extends this:

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Store
    ↓
User Query
    ↓
Query Embedding
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Generated Answer
```

The retrieval stage provides the information that can be supplied to the language model.

---

# 29. Why Day 17 Is Important

Semantic search introduces the basic idea behind modern retrieval systems:

```text
Text
 ↓
Vector Representation
 ↓
Similarity
 ↓
Ranking
 ↓
Retrieval
```

This changes search from:

```text
"What words are present?"
```

to:

```text
"What information is semantically related?"
```

That distinction is fundamental to many modern AI applications.

---

# 30. Key Concepts

### Embedding

A numerical representation of text.

### Sentence Transformer

A model architecture/library used to generate useful sentence embeddings.

### Vector

An ordered collection of numerical values.

### Cosine Similarity

A mathematical measure used to compare vector directions.

### Query Embedding

The vector representation of the user's search query.

### Document Embedding

The vector representation of a stored document.

### Top-K Retrieval

Returning the K highest-ranked results.

### Semantic Search

Searching based primarily on semantic similarity rather than exact keyword matching.

---

# 31. Complete Mental Model

The entire concept can be remembered as:

```text
             DOCUMENTS
                 ↓
          Embedding Model
                 ↓
        Document Embeddings
                 ↓
          Store in Memory
                 │
                 │
                 │
             USER QUERY
                 ↓
          Embedding Model
                 ↓
           Query Embedding
                 ↓
        Compare with Documents
                 ↓
        Cosine Similarity
                 ↓
              Ranking
                 ↓
             Top 3
                 ↓
             Results
```

The core idea is:

```text
Documents → Vectors
Query → Vector
Vectors → Similarity
Similarity → Ranking
Ranking → Search Results
```

---

# 32. Final Takeaway

Semantic search allows an application to retrieve information based on **meaning**.

The fundamental process is:

```text
Documents
    ↓
Embeddings
    ↓
Store Vectors

User Query
    ↓
Query Embedding
    ↓
Similarity Calculation
    ↓
Ranking
    ↓
Top Results
```

The Day 17 project demonstrates the first practical retrieval system using:

- Python
- Sentence Transformers
- `all-MiniLM-L6-v2`
- NumPy
- Cosine Similarity
- Top-K retrieval

The central concept is:

> **Search by meaning, not just keywords.**

---

# 📝 Day 18 — AI Vector Database Search

### 1. What Is a Vector Database?

A **vector database** is a database designed to store, organize, and search numerical vectors.

Text itself cannot be directly compared for meaning. An embedding model converts text into a vector, which is a list of numbers representing the semantic meaning of that text.

For example:

```text
"Terraform manages infrastructure"
            ↓
     Embedding Model
            ↓
[0.12, -0.42, 0.73, 0.18, ...]
```

The vector database stores these vectors and provides efficient similarity search.

The basic idea is:

```text
Text
 ↓
Embedding
 ↓
Vector
 ↓
Vector Database
 ↓
Similarity Search
 ↓
Relevant Documents
```

---

## 2. Why a Vector Database Is Useful

Normal keyword search mainly looks for matching words.

Suppose the query is:

```text
How can cloud infrastructure be automated?
```

A keyword search looks for words such as:

```text
cloud
infrastructure
automated
```

Semantic search works differently.

A document such as:

```text
Terraform allows infrastructure to be managed as code.
```

can be considered highly relevant even though it does not contain the exact words from the question.

This is possible because both the stored document and the query are represented as vectors.

The database searches for vectors that are close in meaning.

---

## 3. Main Components

A vector search system has several important components.

```text
Knowledge Documents
        ↓
Embedding Model
        ↓
Vector Embeddings
        ↓
Vector Database
        ↓
Similarity Search
        ↓
Top-K Results
```

### Embedding Model

The embedding model converts text into vectors.

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

### Vector Database

The vector database stores and retrieves those vectors.

```text
Vector
 ↓
Vector Database
 ↓
Similarity Search
 ↓
Relevant Results
```

These are separate responsibilities.

The embedding model **creates the vector**.

The vector database **stores and searches the vector**.

---

# 4. ChromaDB

**ChromaDB** is a vector database that can run locally.

It is useful for learning and developing AI retrieval applications because a cloud database is not required.

ChromaDB can store:

- Documents
- Embeddings
- Metadata
- IDs

It can also perform similarity searches and persist the database to disk.

---

# 5. Collection

A **collection** is a logical container for related data inside ChromaDB.

For a DevOps knowledge system, a collection can be named:

```text
devops_knowledge
```

Conceptually:

```text
ChromaDB
   │
   └── devops_knowledge
          │
          ├── Document 1
          ├── Document 2
          ├── Document 3
          └── ...
```

A collection keeps related documents, embeddings, and metadata together.

A collection can be created or retrieved using:

```python
collection = client.get_or_create_collection(
    name="devops_knowledge"
)
```

`get_or_create_collection()` is useful because the collection is created if it does not already exist and reused if it already exists.

---

# 6. Knowledge Documents

A small knowledge base can contain documents such as:

```text
AWS EC2 provides scalable virtual servers.

Amazon S3 provides object storage.

Docker packages applications into containers.

Kubernetes manages containerized workloads.

Terraform allows infrastructure to be managed as code.

GitLab CI/CD automates software delivery pipelines.

Amazon RDS provides managed relational databases.
```

Each document can also contain metadata.

Example:

```python
{
    "text": "Terraform allows infrastructure to be managed as code.",
    "category": "DevOps",
    "technology": "Terraform"
}
```

Here:

- `text` contains the actual knowledge.
- `category` identifies the type of technology.
- `technology` identifies the specific technology.

---

# 7. Metadata

**Metadata** means additional information stored about a document.

For example:

```python
{
    "category": "DevOps",
    "technology": "Terraform"
}
```

The document's embedding is used for semantic similarity.

Metadata can be used for additional filtering or organization.

Conceptually:

```text
Document
   │
   ├── Text
   │
   ├── Embedding
   │
   └── Metadata
        ├── Category
        └── Technology
```

Metadata becomes especially useful when a system needs both:

```text
Semantic Search
       +
Structured Filtering
```

For example, a search can later be restricted to documents where:

```text
category = DevOps
```

---

# 8. Sentence Transformers

Sentence Transformers provides models that convert text into meaningful numerical vectors.

A commonly used model is:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

A document can then be converted into an embedding:

```python
text = "Terraform manages infrastructure"

embedding = model.encode(text)

print(embedding)
```

The output is a numerical vector.

The exact numbers are not important individually. Together, they represent the semantic information captured by the model.

---

# 9. Creating the ChromaDB Client

A persistent ChromaDB client can be created using:

```python
import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)
```

The path:

```text
./chroma_db
```

specifies where the local database is stored.

This means the database can remain available after the Python program exits.

The project can therefore contain:

```text
Day-18/
│
├── documents.py
├── semantic_search.py
├── requirements.txt
└── chroma_db/
```

---

# 10. Choosing Cosine Distance

A collection can be configured to use cosine distance:

```python
collection = client.get_or_create_collection(
    name="devops_knowledge",
    metadata={
        "hnsw:space": "cosine"
    }
)
```

Cosine distance measures how different two vectors are based on their direction.

For semantic search, vectors representing similar meanings tend to be closer together.

The important idea is:

```text
Smaller Distance
       ↓
More Similar

Larger Distance
       ↓
Less Similar
```

---

# 11. Generating Document Embeddings

First, extract the document text:

```python
texts = [
    document["text"]
    for document in documents
]
```

Then generate embeddings:

```python
embeddings = model.encode(
    texts,
    normalize_embeddings=True
).tolist()
```

The result is a list of vectors.

Conceptually:

```text
Document 1 → Vector 1
Document 2 → Vector 2
Document 3 → Vector 3
Document 4 → Vector 4
```

These vectors can then be stored in ChromaDB.

---

# 12. Storing Documents

ChromaDB can store documents, embeddings, IDs, and metadata together.

Example:

```python
collection.upsert(
    ids=["doc1", "doc2"],
    documents=texts,
    embeddings=embeddings,
    metadatas=[
        {
            "category": "Cloud",
            "technology": "AWS EC2"
        },
        {
            "category": "DevOps",
            "technology": "Terraform"
        }
    ]
)
```

`upsert()` means:

- Add the data if the ID does not exist.
- Update the data if the ID already exists.

This is useful when the knowledge base may be updated.

---

# 13. What Is an ID?

Every stored record should have an identifier.

For example:

```text
doc1
doc2
doc3
doc4
```

IDs allow individual records to be uniquely identified.

A typical record contains:

```text
ID
Document
Embedding
Metadata
```

---

# 14. Querying the Vector Database

When a user enters a question:

```text
How can cloud infrastructure be automated?
```

the query must also be converted into an embedding.

```python
query_embedding = model.encode(
    query,
    normalize_embeddings=True
).tolist()
```

Now the query is represented as a vector.

The query vector can be sent to ChromaDB:

```python
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)
```

The database searches for the closest stored vectors.

---

# 15. Top-K Retrieval

`n_results=3` means that the three most relevant results should be returned.

This is called **Top-K retrieval**.

```text
Query
 ↓
Similarity Search
 ↓
Top 3 Results
```

For example:

```text
Rank 1 → Terraform
Rank 2 → GitLab CI/CD
Rank 3 → AWS EC2
```

The value of K can be changed:

```python
n_results=5
```

would return the top five results.

---

# 16. Query Flow

The complete search process is:

```text
User Question
      ↓
Sentence Transformer
      ↓
Query Embedding
      ↓
ChromaDB
      ↓
Compare With Stored Vectors
      ↓
Rank Similar Results
      ↓
Top-K Documents
```

The stored documents have already been converted into vectors.

Only the new query needs to be converted before performing the search.

---

# 17. Search Results

ChromaDB can return:

- Matching documents
- Metadata
- Distances
- IDs

Example result information:

```text
Rank 1
Technology: Terraform
Category: DevOps
Similarity: 0.xx
Content: Terraform allows infrastructure to be managed as code.
```

The metadata makes the result easier to understand.

Instead of returning only text, the application can show which technology and category produced the result.

---

# 18. Distance and Similarity

ChromaDB returns a distance value.

When cosine distance is being used, a simple presentation value can be calculated as:

```python
similarity = 1 - distance
```

For example:

```text
Distance = 0.12

Similarity = 1 - 0.12
           = 0.88
```

A lower distance means the vectors are closer.

A higher similarity value means the documents are more semantically similar.

The similarity value should be treated as a ranking signal, not as a guaranteed percentage of correctness.

---

# 19. Why Normalize Embeddings?

The code uses:

```python
normalize_embeddings=True
```

Normalization makes the vectors have unit length.

This is useful when working with cosine-based similarity because the comparison focuses on the direction of the vectors rather than their magnitude.

The important point is that the document embeddings and query embeddings should be generated consistently.

---

# 20. Persistence

A persistent client stores the database locally:

```python
client = chromadb.PersistentClient(
    path="./chroma_db"
)
```

Without persistence, application data may exist only for the current process.

With persistence, the vector database can be loaded again when the application starts.

This is important for a knowledge-search application because documents should not need to be embedded and inserted every time the application starts.

Using `upsert()` also makes repeated application runs safer because existing IDs can be updated instead of blindly creating duplicate records.

---

# 21. Complete Mental Model

The complete system can be understood as four major stages.

### Stage 1 — Prepare Knowledge

```text
Documents
   ↓
Text + Metadata
```

### Stage 2 — Create Embeddings

```text
Text
 ↓
Sentence Transformer
 ↓
Vector
```

### Stage 3 — Store

```text
Vector
   +
Document
   +
Metadata
   ↓
ChromaDB
```

### Stage 4 — Search

```text
User Question
      ↓
Query Embedding
      ↓
ChromaDB Similarity Search
      ↓
Top-K Results
```

---

# 22. Important Terms

### Vector

A numerical representation of information.

```text
[0.12, -0.42, 0.73, ...]
```

### Embedding

A vector generated by an embedding model to represent the meaning of data.

### Embedding Model

A machine-learning model that converts text into embeddings.

### Vector Database

A database designed to store and retrieve vectors based on similarity.

### Collection

A logical group of related records in ChromaDB.

### Metadata

Additional structured information attached to a document.

### Similarity Search

Searching for vectors that are closest to a query vector.

### Top-K

The K most relevant results returned from a search.

### Persistence

Saving the vector database so it can be reused later.

---

# 23. Common Questions

### Is ChromaDB the embedding model?

No.

ChromaDB is the vector database.

The embedding model creates the vectors.

```text
Sentence Transformer
        ↓
Creates Embedding

ChromaDB
        ↓
Stores + Searches Embedding
```

### Does ChromaDB understand the meaning of text by itself?

The semantic representation comes from the embedding model.

ChromaDB receives vectors and performs vector storage and retrieval.

### Does the database store only the vector?

No.

It can store the document, embedding, metadata, and ID together.

### Why store metadata?

Metadata provides additional information and can support filtering and organization.

### Why use Top-K?

Returning every document is usually unnecessary.

Top-K retrieval returns only the most relevant results.

---

# 24. Day 18 Challenge

Extend the knowledge base with technologies such as:

```text
Prometheus
Grafana
Jenkins
Ansible
Azure
Google Cloud
Redis
PostgreSQL
```

Each record should contain:

```python
{
    "text": "...",
    "category": "...",
    "technology": "..."
}
```

Then add:

1. A configurable Top-K value.
2. Metadata filtering.
3. More natural-language questions.
4. Additional categories such as `Cloud`, `DevOps`, and `Database`.

A useful challenge query is:

```text
How can infrastructure deployment be automated?
```

Another useful query is:

```text
Which technology manages containerized applications?
```

The goal is to observe whether the returned documents are semantically relevant rather than simply matching exact words.

---

# 25. Final Architecture

```text
                  KNOWLEDGE DOCUMENTS
                          │
                          ▼
                 ┌─────────────────┐
                 │ Embedding Model │
                 └─────────────────┘
                          │
                          ▼
                     Embeddings
                          │
                          ▼
                 ┌─────────────────┐
                 │     ChromaDB    │
                 │                 │
                 │ Documents       │
                 │ Embeddings      │
                 │ Metadata        │
                 │ IDs             │
                 └─────────────────┘
                          ▲
                          │
                   Query Embedding
                          ▲
                          │
                    User Question
                          │
                          ▼
                 Similarity Search
                          │
                          ▼
                     Top-K Results
```

## 🎯 Core Takeaway

A vector database provides the storage and retrieval layer for semantic search.

The essential flow is:

```text
Document
   ↓
Embedding Model
   ↓
Vector
   ↓
ChromaDB
   ↓
Stored Knowledge

User Question
   ↓
Embedding Model
   ↓
Query Vector
   ↓
ChromaDB
   ↓
Similarity Search
   ↓
Top-K Relevant Documents
```

The most important distinction is:

> **The embedding model creates the vector. The vector database stores and retrieves the vector.**

That separation is the foundation of a practical AI retrieval system.

# 📚 Day 19 — Build a RAG System

## 1. What is RAG?

**RAG** stands for **Retrieval-Augmented Generation**.

RAG combines two processes:

- **Retrieval** → find relevant information from a knowledge base.
- **Generation** → use an LLM to generate an answer from that information.

The basic idea is:

```text
Retrieval + Generation = RAG
```

A normal LLM application:

```text
User Question
      ↓
     LLM
      ↓
   Answer
```

A RAG application:

```text
User Question
      ↓
Query Embedding
      ↓
Vector Database
      ↓
Relevant Documents
      ↓
Context
      ↓
LLM
      ↓
Grounded Answer
```

The important difference is that the LLM receives relevant information retrieved from a knowledge base instead of receiving the entire knowledge base.

---

## 2. Day 19 Objective

The goal is to build a **DevOps Knowledge Assistant**.

The knowledge base contains internal documents such as:

```text
AWS EC2 provides virtual compute capacity.

Amazon S3 is an object storage service.

Amazon RDS provides managed relational databases.

AWS Lambda runs code without provisioning servers.

Docker packages applications into portable containers.

Kubernetes orchestrates containerized workloads.

Terraform allows infrastructure to be defined as code.

GitLab CI/CD automates software build and deployment pipelines.
```

The application should answer questions using these documents.

The knowledge source is **internal ChromaDB only**.

There is no web search or external document retrieval.

---

## 3. Complete Architecture

```text
                Internal Knowledge Base
                         ↓
                    Documents
                         ↓
                    Embeddings
                         ↓
                      ChromaDB
                         ↑
                         │
User Question → Query Embedding
                         ↓
                  Similarity Search
                         ↓
                  Relevant Documents
                         ↓
                      Context
                         ↓
                      Gemini
                         ↓
                  Grounded Answer
                         ↓
                      Sources
```

Each component has a specific responsibility:

| Component | Responsibility |
|---|---|
| Documents | Store internal knowledge |
| Sentence Transformers | Create embeddings |
| ChromaDB | Store and retrieve vectors |
| Query embedding | Represent the user's question |
| Similarity search | Find relevant documents |
| Context | Retrieved information given to Gemini |
| Gemini | Generate the final answer |
| Sources | Show which documents supported the answer |

---

# 4. Internal Knowledge Base

The knowledge base is the source of truth.

Example:

```python
documents = [
    "AWS EC2 provides virtual compute capacity.",
    "Amazon S3 is an object storage service.",
    "Amazon RDS provides managed relational databases.",
    "AWS Lambda runs code without provisioning servers.",
    "Docker packages applications into portable containers.",
    "Kubernetes orchestrates containerized workloads.",
    "Terraform allows infrastructure to be defined as code.",
    "GitLab CI/CD automates software build and deployment pipelines."
]
```

These documents are converted into embeddings and stored in ChromaDB.

---

# 5. Document Embeddings

An embedding represents text as a numerical vector.

For example:

```text
"Terraform allows infrastructure to be defined as code."
                         ↓
                    Embedding Model
                         ↓
                 [0.21, -0.13, 0.82, ...]
```

The vector captures the semantic meaning of the document.

The same embedding model must be used when creating document embeddings and query embeddings.

Example:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embedding = model.encode(
    "Terraform allows infrastructure to be defined as code."
)
```

---

# 6. ChromaDB

ChromaDB is used as the vector database.

Documents and their embeddings are stored together.

Example:

```python
import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.create_collection(
    name="day19_devops_knowledge"
)
```

Documents can then be stored:

```python
collection.add(
    ids=["doc_1"],
    documents=[
        "Terraform allows infrastructure to be defined as code."
    ],
    embeddings=[embedding.tolist()]
)
```

The database allows semantic similarity searches.

---

# 7. Query Embedding

When a user asks:

```text
How can infrastructure be automated?
```

The question is also converted into an embedding.

```python
query_embedding = model.encode(
    question
).tolist()
```

The query vector is compared with the document vectors stored in ChromaDB.

This allows semantic matching rather than simple keyword matching.

For example:

```text
Question:
How can infrastructure be automated?

Relevant document:
Terraform allows infrastructure to be defined as code.
```

The words are different, but their meaning is related.

---

# 8. Similarity Search

The query embedding is sent to ChromaDB:

```python
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)
```

`n_results=3` means that up to three relevant documents are requested.

The result contains documents and their distances.

Example:

```text
1. Terraform allows infrastructure to be defined as code.
2. GitLab CI/CD automates software build and deployment pipelines.
3. Docker packages applications into portable containers.
```

The retrieved documents become the context for the LLM.

---

# 9. Why Top-K Retrieval is Used

Sending the entire knowledge base to Gemini is unnecessary.

Instead of:

```text
8 documents
   ↓
Gemini
```

the application retrieves only the most relevant documents:

```text
8 documents
   ↓
Similarity Search
   ↓
Top 3 relevant documents
   ↓
Gemini
```

This reduces unnecessary context and focuses the model on relevant information.

---

# 10. Relevance Threshold

Similarity search always returns the closest available documents.

Even an unrelated question may return something.

For example:

```text
Question:
What is AWS CloudFront?

Possible results:
S3
EC2
Lambda
```

These documents may simply be the closest available vectors.

Therefore a distance threshold can be used:

```python
MAX_DISTANCE = 0.8
```

Only documents satisfying the configured threshold are accepted.

Conceptually:

```text
Query
  ↓
Top-K Candidates
  ↓
Distance Check
  ↓
Relevant?
 ┌───────────┴───────────┐
Yes                       No
 ↓                         ↓
Context              No Context
 ↓                         ↓
Gemini              "Not found"
```

The exact threshold depends on the embedding model and data and may require tuning.

---

# 11. Building the Context

After retrieval, the documents are combined:

```python
context = "\n\n".join(
    retrieved_documents
)
```

For example:

```text
Terraform allows infrastructure to be defined as code.

GitLab CI/CD automates software build and deployment pipelines.
```

This becomes the context sent to Gemini.

---

# 12. Grounded Generation

The LLM prompt must clearly restrict the answer to the retrieved context.

Example:

```text
You are an internal DevOps knowledge assistant.

Answer the question using ONLY the provided
internal knowledge.

Do not use general knowledge.
Do not invent information.
Do not use information outside the context.

Internal Knowledge:
-------------------------
Terraform allows infrastructure to be defined as code.
-------------------------

Question:
How can infrastructure be automated?

Give a concise answer.
```

The model should generate:

```text
Terraform can be used to automate infrastructure
by defining infrastructure as code.
```

The important concept is:

> **The retrieved context becomes the evidence used for generation.**

---

# 13. Gemini's Role

Gemini is the **generation component**, not the knowledge database.

The responsibilities are separated:

```text
ChromaDB
    ↓
Retrieval

Gemini
    ↓
Generation
```

ChromaDB answers:

> Which internal documents are relevant?

Gemini answers:

> How can the retrieved information be expressed as a useful response?

---

# 14. Source Attribution

A RAG system should return the documents used to generate the answer.

Example:

```json
{
  "answer": "Terraform can be used to automate infrastructure by defining infrastructure as code.",
  "sources": [
    "Terraform allows infrastructure to be defined as code."
  ]
}
```

This provides basic traceability:

```text
Answer
  ↓
Retrieved Context
  ↓
Source Document
```

The sources should come from the retrieved internal documents, not from Gemini's general knowledge.

---

# 15. Hallucination Protection

Consider:

```text
Question:
What is AWS CloudFront?
```

The internal knowledge base contains no CloudFront information.

The expected response is:

```text
I couldn't find relevant information about this
in the provided knowledge base.
```

Sources:

```json
[]
```

The application should not allow Gemini to answer:

```text
AWS CloudFront is a content delivery network...
```

because that information is outside the provided knowledge base.

This demonstrates **grounded generation**.

---

# 16. Complete RAG Flow

For:

```text
How can I automate infrastructure?
```

the complete process is:

```text
1. User asks a question
            ↓
2. Create query embedding
            ↓
3. Search ChromaDB
            ↓
4. Retrieve relevant documents
            ↓
5. Apply relevance threshold
            ↓
6. Build context
            ↓
7. Send context + question to Gemini
            ↓
8. Generate grounded answer
            ↓
9. Return answer + sources
```

---

# 17. Important Code Pattern

The central retrieval logic is:

```python
query_embedding = embedding_model.encode(
    question
).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

retrieved_documents = results["documents"][0]
```

The central generation logic is:

```python
context = "\n\n".join(
    retrieved_documents
)

response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents=prompt
)

answer = response.text
```

The two operations together form the basic RAG pipeline.

---

# 18. Example End-to-End Execution

### Question

```text
Which AWS service should be used for storing files?
```

### Query Embedding

```text
Question
   ↓
Embedding Model
   ↓
Query Vector
```

### Retrieval

ChromaDB finds:

```text
Amazon S3 is an object storage service.
```

### Context

```text
Amazon S3 is an object storage service.
```

### Generation

Gemini receives the context and question.

### Answer

```text
Amazon S3 is suitable for storing files because
it is an object storage service.
```

### Source

```text
Amazon S3 is an object storage service.
```

---

# 19. Key Principles

### Retrieval before generation

The LLM should receive relevant information before generating the answer.

### Context controls the answer

The retrieved documents should define what information the model can use.

### Internal knowledge is the source of truth

ChromaDB contains the application's knowledge.

### The LLM is not the database

Gemini generates language; ChromaDB retrieves knowledge.

### Sources improve traceability

Returning retrieved documents makes it possible to understand what supported an answer.

### Relevance matters

Poor retrieval produces poor context, which can produce poor answers.

---

# 20. Final Concept

The complete idea of Day 19 can be summarized as:

```text
Internal Knowledge
       ↓
    Embeddings
       ↓
    ChromaDB
       ↓
    Retrieval
       ↓
Relevant Context
       ↓
     Gemini
       ↓
Grounded Answer
       +
    Sources
```

**RAG = Retrieval + Generation**

The retrieval stage finds the relevant internal knowledge, and the generation stage uses that knowledge to produce a natural-language answer.
