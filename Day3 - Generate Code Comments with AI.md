# Day3 - Generate Code Comments with AI

AI Comment Generator

The nautilus AI Development Team is exploring how artificial intelligence can improve code readability and maintainability by automatically generating meaningful comments. You are tasked with building a Python-based AI module that analyzes a code snippet and produces a clear, one-line comment or docstring describing its purpose.

Inside /root/openaiproject/commenter.py, create an OpenAI client using the API key and base URL provided in /root/.bash_profile. Define a function generate_comment(code_snippet: str) -> str that constructs a parameterized prompt instructing the AI to generate a one-line comment explaining the provided code.

After building the function, send the constructed prompt to the OpenAI chat model:

model: openai/gpt-4.1-mini
messages: user → prompt
max_tokens: 30
temperature: 0.2
Save the result in a variable named response and print the generated comment or docstring to the console.

Use the following snippet for testing inside your script:

def calculate_area(length, width):
 return length * width


Notes:

Ensure you are working inside /root/openaiproject.

api_key and base_url are stored in /root/.bash_profile.

The function must be parameterized using the input snippet.

The function must return the generated comment AND print it.

Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

Before running, create a virtual environment and install OpenAI:

python3 -m venv venv && source venv/bin/activate && pip install openai

You are allowed up to 10 OpenAI requests. Past this limit you may encounter a rate limiter error, so optimize your request usage.

## Objective

Build a Python-based AI module that analyzes a code snippet and generates a clear, one-line comment or docstring describing its purpose.

## File

`/root/openaiproject/commenter.py`

## Implementation

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE")
)


def generate_comment(code_snippet: str) -> str:
    prompt = f"""
Generate a clear, concise one-line comment or docstring explaining the purpose
of the following Python code. Return only the comment/docstring, with no extra
explanation.

Code:
{code_snippet}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=30,
        temperature=0.2
    )

    comment = response.choices[0].message.content.strip()
    print(comment)
    return comment


code = """def calculate_area(length, width):
    return length * width"""

generate_comment(code)
```

## Setup

```bash
cd /root/openaiproject

python3 -m venv venv
source venv/bin/activate

pip install openai
```

## Run

```bash
python commenter.py
```

## Test Code

```python
def calculate_area(length, width):
    return length * width
```

## Expected Output

The generated output should be a one-line comment/docstring describing the purpose of the function, for example:

```text
# Calculates the area of a rectangle using its length and width.
```
### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/6e531736-b32d-4a04-809d-28adaad1a417" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/410d1d7d-3343-458a-a167-254dbd3a4328" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/52ffdfa9-0ffd-4e66-86f6-3bf778b378ef" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/3ece65fd-0559-4f9e-958f-6276a23221d3" />




