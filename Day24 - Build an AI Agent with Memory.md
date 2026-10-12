 # 🚀 Day 24 — Build an AI Agent with Memory 🧠

- a Local AI Agent with Short-Term Memory

## 1\. Project Overview

Build a local AI agent using Python, Ollama, and Llama 3.2 that remembers previous messages during a conversation and uses them to answer follow-up questions.

## 2\. Problem Statement

Without memory, an AI agent may forget the context of earlier messages. With short-term memory, it can use previous questions and answers to provide relevant, context-aware responses.

**Example:**

- User: My production server has high disk usage.
- Agent: Check which directories are consuming the most space.
- User: What should I check first?
- Agent: Start by running `du -sh /* 2>/dev/null` to identify directories using the most disk space.

## 3\. How It Works

1. The user enters a message.
2. The agent adds it to conversation history.
3. Python sends the conversation history to Ollama.
4. Llama 3.2 generates a response using the previous messages.
5. The response is saved in memory for the next interaction.

## 4\. Features

- Short-term conversation memory.
- Context-aware follow-up questions.
- Conversation history management.
- Memory reset using `/reset`.
- Memory inspection using `/memory`.
- Help command using `/help`.
- Exit command using `/exit`.
- Limited conversation history to control context size.
- Local execution using Ollama.

## 5\. Technology Stack

- Python 3.10+
- Ollama
- Llama 3.2
- Python lists and dictionaries
- `requests` library

## 6\. Project Structure

```
Day-24/
├── main.py
└── requirements.txt
```

## 7\. File Contents

### File 1: `requirements.txt`

```
ollama
```

### File 2: `main.py`

```
import requests

MODEL_NAME = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/chat"
MAX_HISTORY = 10

SYSTEM_PROMPT = """
You are a helpful local AI DevOps assistant.
Remember the conversation context provided in the messages.
Answer follow-up questions using previous messages.
Provide clear, practical, and safe technical guidance.
"""

def ask_agent(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )
    response.raise_for_status()

    return response.json()["message"]["content"]

def main():
    print("=" * 55)
    print("Day 24 - Local AI Agent with Short-Term Memory")
    print(f"Model: {MODEL_NAME}")
    print("=" * 55)

    print("Commands: /help, /memory, /reset, /exit")
    print("Ask a question to start the conversation.\n")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input == "/exit":
                print("Goodbye!")
                break

            if user_input == "/help":
                print(
                    "Commands:\n"
                    "/help   - Show available commands\n"
                    "/memory - Display conversation history\n"
                    "/reset  - Clear conversation memory\n"
                    "/exit   - Exit the agent"
                )
                continue

            if user_input == "/memory":
                for message in messages[1:]:
                    role = message["role"].capitalize()
                    print(f"{role}: {message['content']}")
                continue

            if user_input == "/reset":
                messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    }
                ]
                print("Conversation memory cleared.")
                continue

            messages.append({
                "role": "user",
                "content": user_input
            })

            # Keep only the latest conversation messages.
            messages = [messages[0]] + messages[-MAX_HISTORY:]

            print("\nAgent: ", end="", flush=True)

            answer = ask_agent(messages)
            print(answer, "\n")

            messages.append({
                "role": "assistant",
                "content": answer
            })

            # Keep history within the configured limit.
            messages = [messages[0]] + messages[-MAX_HISTORY:]

        except requests.exceptions.ConnectionError:
            print(
                "\nError: Cannot connect to Ollama. "
                "Make sure Ollama is running.\n"
            )

        except requests.exceptions.Timeout:
            print("\nError: The model request timed out.\n")

        except requests.exceptions.RequestException as error:
            print(f"\nOllama request error: {error}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
```

## 8\. Installation and Execution

Open a terminal in the `Day-24` directory.

**Step 1: Create and activate a virtual environment**

```
python -m venv venv
```

Windows Git Bash:

```
source venv/Scripts/activate
```

Windows PowerShell:

```
.\venv\Scripts\Activate.ps1
```

**Step 2: Install dependencies**

```
pip install -r requirements.txt
```

**Step 3: Install and start Ollama**

Download Ollama from https://ollama.com and pull the model:

```
ollama pull llama3.2
```

Ensure Ollama is running locally.

**Step 4: Run the agent**

```
python main.py
```

## 9\. Testing

Try the following conversation:

```
You: My production server has high disk usage.
Agent: Start by identifying which directories consume the most disk space.

You: What should I check first?
Agent: Start with disk-usage analysis, focusing on the largest directories.

You: /memory
Agent: Displays the recent conversation history.

You: /reset
Agent: Conversation memory cleared.

You: What server issue did I mention?
Agent: I don't have that information in the current conversation.
```

_Exact responses depend on the model._

## 10\. Learning Outcomes

- Understand short-term AI memory.
- Pass conversation history to an LLM.
- Use Python lists and dictionaries for message storage.
- Manage the model's context window.
- Implement conversation reset and inspection commands.
- Run a local AI agent without a cloud API.

## 11\. Important Notes

- Memory is stored in Python RAM and is cleared when the program exits.
- `/reset` clears the current conversation.
- `MAX_HISTORY` limits the number of recent messages retained; the system prompt is preserved separately.
- This is short-term conversational memory, not persistent memory across restarts.
- The agent provides suggestions only. Review commands carefully before executing them on production systems.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/d774c2e4-0b32-4aa1-b5e9-f2f40438ca89" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/0dc05127-448b-4093-916f-145231c478ae" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/167ed478-255d-4131-b4fa-27c7ef4c0e78" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/72bbeca5-c21a-472a-9d35-f161ba01c5c9" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/ae54e3f7-b213-41df-a3cf-44deba3c356d" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/d94eb25e-03be-4f8e-a7e2-f288fecc621e" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/fc4d596c-acfb-448b-aead-0ab89d29bc2f" />
