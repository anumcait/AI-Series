# Day 6 - Use AI as an Email Assistant

The datacenter AI Development Team is now working on automating written communication tasks. As part of this initiative, you are required to build a Python-based AI Email Assistant that rewrites messages into polite and professional emails.

Inside email_assistant.py, create an OpenAI client using the provided API key and base URL under /root/.bash_profile. Then, define a function named rewrite_email(text: str) -> str that constructs a parameterized prompt asking the AI to rewrite the given email text politely and professionally.

After defining rewrite_email, send the constructed prompt to the OpenAI chat model with these parameters:

model: openai/gpt-4.1-mini
messages: user → prompt
max_tokens: 60
temperature: 0.1
Store the output in a variable named response and print the polite rewritten email to the console.

Use the following email text for rewriting:

hey send me that report asap


Notes:

Function should accept one parameter: text.

Use the provided OpenAI API key and base_url under /root/.bash_profile.

File email_assistant.py must be inside /root/openaiproject.

Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

Before running the script,use the following commands install OpenAI:

python3 -m venv venv && source venv/bin/activate && pip install openai

You are allowed a maximum of 10 requests before rate limiting may occur.

## Objective

The task was to build a Python-based AI Email Assistant that rewrites messages into polite and professional emails using the OpenAI API.

## Setup

Created and activated a Python virtual environment and installed the OpenAI package:

```bash
cd /root/openaiproject
python3 -m venv venv
source venv/bin/activate
source /root/.bash_profile
pip install openai
```

## Check Available Models

The available models can be checked with:

```bash
echo "$ALLOWED_MODELS"
```

The compatible model used for this task was:

```text
openai/gpt-4.1-mini
```

## `/root/openaiproject/email_assistant.py`

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
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.1,
    )

    return response.choices[0].message.content.strip()


text = "hey send me that report asap"

response = rewrite_email(text)
print(response)
```

## Run

```bash
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
python email_assistant.py
```

## Input

```text
hey send me that report asap
```

## Output

```text
Could you please send me that report as soon as possible? Thank you.
```

## Result

The AI Email Assistant successfully rewrites the provided informal message into a polite and professional email using the OpenAI-compatible API.

## Completion

- Created `email_assistant.py`
- Configured the OpenAI client with the provided API key and base URL
- Implemented `rewrite_email(text: str) -> str`
- Created a parameterized rewriting prompt
- Used the `openai/gpt-4.1-mini` model
- Set `max_tokens=60`
- Set `temperature=0.1`
- Stored the API result in `response`
- Printed the rewritten email to the console
- Successfully transformed the supplied informal email into professional wording

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/20430c80-6a2a-4ab8-af85-074e296a6ec7" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/47f65c8f-bb59-4526-baed-5608eb8eb43f" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/bd9129cd-626d-4232-869b-51689f6336af" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/0d17bdf9-08ef-4fde-8da1-c0c96e8411ad" />




