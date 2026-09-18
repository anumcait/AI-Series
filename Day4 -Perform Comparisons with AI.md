# Day 4 - Perform Comparisons with AI

AI Comparison Lab

The devops AI Development Team is now exploring how artificial intelligence can assist in making smarter, data-driven decisions for cloud optimization. Continuing this journey, you are tasked to build a Python-based AI module that compares chipset used between two major iPhone models.

Inside compare.py, create an OpenAI client using the provided api_key and base_url under /root/.bash_profile. Then, define a function named compare(item1: str, item2: str) -> str that constructs a parameterized prompt asking the AI to compare the two given iPhone models (item1 and item2) in terms of only the chip used, ensuring the response is given in one word only.

Use the following items for comparison:

iphone 13
iphone 17

After defining the function, send the constructed prompt to the OpenAI chat model using:

model: openai/gpt-4.1-mini
messages: user → prompt
max_tokens: 100
temperature: 0.5
Store the result in a variable named response, and print the one-word comparison output to the console.

Finally, run your compare.py file to perform the chip comparison.


Notes:

Function should accept two parameters: item1 and item2.

Use the provided OpenAI api_key and base_url under /root/.bash_profile.

File compare.py must be inside /root/openaiproject.

Use hardcoded values for api_key and base_url when initializing the OpenAI client or read them from environment variables via os.environ.get('OPENAI_API_KEY') and os.environ.get('OPENAI_API_BASE').

Before running the script run the following commands:

python3 -m venv venv && source venv/bin/activate && pip install openai

You are allowed a maximum of 10 requests. After this, you may encounter a rate limiter error, so use your calls wisely.

## Objective

Build a Python-based AI module that compares the chipset used in two iPhone models.

## Models Compared

- iPhone 13
- iPhone 17

## OpenAI Configuration

The OpenAI client uses:

- API key from `OPENAI_API_KEY`
- Base URL from `OPENAI_API_BASE`
- Model: `openai/gpt-4.1-mini`
- `max_tokens`: `100`
- `temperature`: `0.5`

## Python Function

The `compare()` function accepts two parameters:

```python
def compare(item1: str, item2: str) -> str:
```

It sends a parameterized prompt to the OpenAI chat model and returns the chip name as a single word.

## Execution

The script was executed with:

```bash
python compare.py
```

## Result

```text
A17
```

The comparison successfully returned `A17`.

### Screenshots
