# Day2 - Create an AI Chatbot
AI ChatBot

The AI development team at Nautilus is tasked with building a role-play chatbot using OpenAI's API.

Task Requirements:

Navigate to the /root/openaiproject/chatbot.py directory.

Create a client instance using api_key and base_url.

Use openai model=openai/gpt-4.1-mini

Define a variable prompt with the following content:

You are a friendly travel guide. Greet the user and ask where they want to go.

Send this prompt to the OpenAI chat model and store the result in variable nameresponse.

Extract and print the generated text reply from the response

Run the file after installing OpenAI in a virtual environment.


Notes:

Ensure you are working inside /root/openaiproject.

api_key&base_url are in /root/.bash_profile (typically OPENAI_API_KEY and OPENAI_API_BASE).

Install OpenAI inside a venv before running the script.

python3 -m venv venv && source venv/bin/activate && pip install openai

Use temperature=0.7&max_tokens=100.

Use hardcoded values for api_key&base_url when initializing the OpenAI client, or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error. Therefore, use your requests judiciously.

# AI Chatbot

## Task

Create a role-play travel-guide chatbot using OpenAI's API.

## Requirements

- Work inside `/root/openaiproject`.
- Create `chatbot.py`.
- Create an OpenAI client using `api_key` and `base_url`.
- Read credentials from:
  - `OPENAI_API_KEY`
  - `OPENAI_API_BASE`
- Use the model `openai/gpt-4.1-mini`.
- Define the prompt:
  > You are a friendly travel guide. Greet the user and ask where they want to go.
- Send the prompt to the OpenAI chat model.
- Store the response in a variable named `nameresponse`.
- Extract and print the generated text reply.
- Use `temperature=0.7`.
- Use `max_tokens=100`.
- Install OpenAI inside a Python virtual environment before running the script.

## Setup

```bash
cd /root/openaiproject

python3 -m venv venv
source venv/bin/activate
pip install openai
```

## `chatbot.py`

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

## Run

```bash
source /root/.bash_profile
source venv/bin/activate
python chatbot.py
```

## Expected Behavior

The program should call the OpenAI chat model and print a friendly travel-guide greeting that asks the user where they want to go.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/ee26a4d9-df21-410a-9ef3-e08a6534548e" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/1ff132b3-d1b4-4392-9194-07ab4bbc53e7" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/1e7b0262-b076-45ed-a153-98d083df60aa" />



