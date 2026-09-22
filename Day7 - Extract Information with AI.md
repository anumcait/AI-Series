# Day 7 - Extract Information with AI
Resume Extractor

The devops AI Innovation Team is building a smart Resume Analyzer that automatically extracts the most relevant job keywords from candidate profiles.

You are required to build a Python-based AI module that extracts exactly five comma-separated job-relevant keywords from a resume paragraph.

Inside /root/openaiproject/resume_extractor.py, create an OpenAI client using the provided API key and base URL. Then define a function:

extract_keywords(text: str) -> str

This function must construct a parameterized prompt that asks the AI to extract exactly 5 comma-separated keywords from the provided resume text.

Next, send the prompt to the OpenAI chat model using:

model: openai/gpt-4.1-mini
messages: user → prompt
max_tokens: 40
temperature: 0
Finally, print the extracted keywords.


Notes:

Function must be named extract_keywords.

Use the OpenAI API key and base_url from /root/.bash_profile.

The prompt MUST demand exactly five comma-separated keywords.

Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE')

Before running the script, create & activate a virtual environment and install OpenAI.

python3 -m venv venv&&source venv/bin/activate &&pip install openai

You will use the following resume text:
Experienced DevOps engineer skilled in Python, Kubernetes, Docker, CI/CD pipelines, and cloud automation.
You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error, so use your calls wisely.

## Objective

Build a Python-based AI Resume Extractor that accepts a resume paragraph and uses an OpenAI-compatible AI model to extract exactly five job-relevant keywords.

The keywords must be returned as a single comma-separated string.

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

## `/root/openaiproject/resume_extractor.py`

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

## Run

Activate the environment and load the configuration:

```bash
cd /root/openaiproject
source venv/bin/activate
source /root/.bash_profile
```

Run the script:

```bash
python resume_extractor.py
```

## Input

```text
Experienced DevOps engineer skilled in Python, Kubernetes, Docker, CI/CD pipelines, and cloud automation.
```

## Output

The program must return exactly five comma-separated job-relevant keywords, for example:

```text
Python, Kubernetes, Docker, CI/CD, Cloud Automation
```

The exact keywords may vary because they are selected by the AI, but the output must contain exactly five comma-separated keywords.

## Key Requirements

- Function name: `extract_keywords`
- Input type: `str`
- Return type: `str`
- Model: `openai/gpt-4.1-mini`
- Messages: `user → prompt`
- `max_tokens=40`
- `temperature=0`
- Exactly five keywords
- Keywords must be comma-separated
- No explanations or numbering in the AI output
- API key read from `OPENAI_API_KEY`
- API base URL read from `OPENAI_API_BASE`

## Result

The Resume Extractor demonstrates how an AI model can convert unstructured resume information into a simple structured output that can be used for job matching, candidate analysis, or keyword-based recruitment systems.

## Completion

- Created `resume_extractor.py`
- Created the OpenAI client
- Read API configuration from environment variables
- Implemented `extract_keywords(text: str) -> str`
- Created a parameterized resume-extraction prompt
- Required exactly five comma-separated keywords
- Used `openai/gpt-4.1-mini`
- Set `max_tokens=40`
- Set `temperature=0`
- Printed the extracted keywords

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/c39fa747-cc41-4e12-994c-ea085659a5f7" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/4bb83c2a-fbd7-40d6-aec4-266987addbe0" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/66191418-5b90-444e-9f1c-5febdb7186c9" />




