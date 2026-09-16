### Day1 - Clarify Bugs with AI

Bug Description Clarifier

The nautilus AI Engineering team is developing tools to improve the clarity of developer-reported bugs. Developers often report issues informally, which makes them difficult to understand or reproduce.

You are tasked to build a Python-based AI Bug Description Clarifier that transforms such informal bug reports into clear, structured, and professional issue summaries.

Inside /root/openaiproject/bug_clarifier.py:

Initialize the OpenAI client using environment values (api_key and base_url).

Define a function clarify_bug(description: str) -> str that builds a parameterized prompt to rewrite the raw bug description.

Send this prompt to the OpenAI Chat Completion API.

Use the following configuration for the API call:

model: openai/gpt-4.1-mini
messages: user → the constructed prompt
max_tokens: 100
temperature: 0.0
Use the input bug report:

  App keeps crashing when I click save.

Store the AI response in a variable named response and print the clarified bug summary to the console.

Notes:

Function must use the developer's input description dynamically in the prompt.

Ensure you are working inside /root/openaiproject.

OpenAI credentials are available in /root/.bash_profile.

Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

Before running bug_clarifier.py, set up a virtual environment:

python3 -m venv venv && source venv/bin/activate && pip install openai

Maximum of 10 API requests allowed before rate limiting.

## Objective

The AI Bug Description Clarifier transforms informal developer bug reports into clear, structured, and professional issue summaries.

### Python Implementation

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

### Result

The informal report:

> App keeps crashing when I click save.

was clarified as:

> **Bug Summary:** Application crashes upon clicking the "Save" button.
>
> **Triggering Action:** User clicks the "Save" button within the application.
>
> **Observed Behavior:** The application unexpectedly crashes immediately after the "Save" button is clicked.
