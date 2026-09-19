# Day 5 - Convert Data with AI

AI Converter

The devops AI Development Team is now exploring how artificial intelligence can assist in improving productivity and communication by transforming lengthy text into clear, concise bullet points for faster understanding.

You are tasked to build a Python-based AI module that converts a given paragraph into concise, easy-to-read bullet points.

Inside /root/openaiproject/converter.py, create an OpenAI client using the api_key and base_url provided for this session. Then, define a function named convert_to_bullets(text: str) -> str that constructs a parameterized prompt asking the AI to convert the given paragraph into short, meaningful bullet points.

After creating the function, send the constructed prompt to the OpenAI chat model with the following parameters:

model: openai/gpt-4.1
messages: user → prompt
max_tokens: 150
temperature: 0.1
Store the result in a variable named response and print the bullet points to the console.

Use this paragraph for conversion:

Artificial Intelligence is transforming industries by automating tasks, improving decision-making, and enabling new innovations across healthcare, finance, and education.


Notes:

Function must accept one parameter: text.

Use the provided OpenAI api_key and base_url from /root/.bash_profile.

The prompt must be parameterized with the paragraph.

Use hardcoded values for api_key&base_url when initializing the OpenAI client, or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

Before running converter.py, create and activate a virtual environment:

python3 -m venv venv && source venv/bin/activate && pip install openai

You are allowed a maximum of 10 API requests due to rate limits.

## Objective

Build a Python-based AI module that converts a paragraph into concise, easy-to-read bullet points using the OpenAI API.

## Setup

Create and activate a virtual environment and install the OpenAI package:

```bash
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

For this environment, `openai/gpt-4.1-mini` was available while `openai/gpt-4.1` was not. Therefore, the compatible model was used.

## `/root/openaiproject/converter.py`

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

## Run

```bash
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
python converter.py
```

## Output

```text
- AI automates tasks across industries
- Enhances decision-making processes
- Drives innovations in healthcare, finance, and education
```

## Result

The AI Converter successfully transforms the supplied paragraph into concise bullet points using the OpenAI-compatible API.

### Screenshots

