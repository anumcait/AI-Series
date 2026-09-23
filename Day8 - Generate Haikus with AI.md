# Day 7 - Generate Haikus with AI

Haiku Generator

The xfusion AI Development Team is experimenting with how artificial intelligence can create expressive short poetry through automation. In this task, you are required to build a Python-based AI module that generates three-line haikus (5-7-5 syllable pattern) based on a given topic.

Inside /root/openaiproject/haiku_generator.py, create an OpenAI client using the api_key and base_url provided for this session. Additionally, define a function named generate_haiku(topic: str) -> str. This function should construct a parameterized prompt that instructs the AI to generate a haiku about the specified topic, strictly following the 5-7-5 syllable structure.

Then, send the parameterized prompt to the OpenAI chat model using:

model: openai/gpt-4.1-mini
prompt: parameterized_prompt
max_tokens: 60
temperature: 0.0
Store the output in a variable named response and print the generated haiku (three distinct lines). Use the topic:

Topic: 'sky'


Notes:

Function should accept one parameter: topic.

Use the provided OpenAI  api_key and base_url under /root/.bash_profile.

The prompt must be parameterized with the topic.

Ensure you are working inside /root/openaiproject.

Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

Before running, create and activate a virtual environment and install OpenAI:

python3 -m venv venv && source venv/bin/activate && pip install openai

Final output should display three distinct lines (the haiku).

You are allowed a maximum of 10 requests before hitting rate limits.

## Objective

Build a Python-based AI Haiku Generator that accepts a topic and uses an OpenAI-compatible AI model to generate a three-line haiku.

The haiku must strictly follow the **5-7-5 syllable pattern**.

## Setup

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

Load the API configuration:

```bash
source /root/.bash_profile
```

Install the OpenAI package:

```bash
pip install openai
```

## Check Available Models

The available models can be checked with:

```bash
echo "$ALLOWED_MODELS"
```

The model used for this task was:

```text
openai/gpt-4.1-mini
```

## `/root/openaiproject/haiku_generator.py`

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

## Run

Activate the environment and load the configuration:

```bash
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
```

Run the script:

```bash
python haiku_generator.py
```

## Input

```text
Topic: sky
```

## Output

The program must display exactly three distinct lines forming a haiku with a **5-7-5 syllable structure**, for example:

```text
Blue sky spreads above
Soft clouds drift across the blue
Sun warms earth below
```

## Key Requirements

- Function name: `generate_haiku`
- Function signature: `generate_haiku(topic: str) -> str`
- Input type: `str`
- Return type: `str`
- Model: `openai/gpt-4.1-mini`
- Prompt must be parameterized with `topic`
- `max_tokens=60`
- `temperature=0.0`
- Exactly three lines in the generated output
- 5 syllables on line 1
- 7 syllables on line 2
- 5 syllables on line 3
- API key read from `OPENAI_API_KEY`
- API base URL read from `OPENAI_API_BASE`
- Output stored in a variable named `response`
- Generated haiku printed to the terminal

## Result

The Haiku Generator demonstrates how an AI model can generate structured short-form poetry from a user-provided topic while following a specified three-line 5-7-5 syllable format.

## Completion

- Created `haiku_generator.py`
- Created the OpenAI client
- Read API configuration from environment variables
- Implemented `generate_haiku(topic: str) -> str`
- Created a parameterized haiku-generation prompt
- Used topic `sky`
- Used `openai/gpt-4.1-mini`
- Set `max_tokens=60`
- Set `temperature=0.0`
- Stored the model output in `response`
- Printed the generated three-line haiku
