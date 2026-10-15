
# Day 26 — AI Agent with Persistent Memory

## Objective

Build a local Personal Learning Assistant using Python, Ollama, and Llama 3.2:3b that stores useful facts and retrieves them when answering questions.

## Technologies Used

- **Python** — Application logic and memory management.
- **Ollama** — Runs the local language model.
- **Llama 3.2:3b** — Generates context-aware answers.
- **JSON** — Stores memories permanently in a local file.
- **Requests** — Connects Python to the Ollama API.

## What We Built

### 1\. Persistent Memory Storage

Created `memories.json` to store facts with timestamps. Memories remain available after closing and restarting the application.

### 2\. Memory Management

Implemented Python functions to save, load, display, and delete memories. Exact duplicate facts are prevented, and invalid memory data is handled safely.

### 3\. Memory Retrieval

Implemented keyword-based retrieval to find saved facts relevant to a user's question. The retrieved facts are added to the LLM prompt before generating an answer.

### 4\. Ollama Integration

Connected Python to Ollama's chat API using the `llama3.2:3b` model to generate answers using retrieved memories.

### 5\. Application Commands

Implemented the following commands:

- `remember: <fact>` — Save a new memory.
- `/memory` — Display saved memories.
- `/forget` — Delete a selected memory.
- `/reset` — Delete all memories after confirmation.
- `/exit` — Exit the application.

## How to Run

1. Ensure Ollama is installed and the model is available:

```
   ollama pull llama3.2:3b
```

2. Install the Python dependency:

```
   python -m pip install requests
```

3. Start the application:

```
   python main.py
```

## Testing Performed

- Saved a fact using the `remember:` command.
- Verified saved facts using `/memory`.
- Asked questions to test memory retrieval.
- Verified that memories persisted after restarting the application.
- Tested duplicate prevention and memory deletion commands.

## Key Learning

**Short-term memory** exists within the current conversation, whereas **persistent memory** survives application restarts.

Saving information is only one part of persistent memory. The application must also retrieve relevant facts and provide them to the LLM as context to generate personalized answers.

## Current Limitations

- Facts must be saved explicitly using `remember:`.
- Retrieval uses basic keyword matching, so differently worded questions may not find the correct memory.
- Automatic memory extraction and semantic search are potential future improvements.

## Result

Successfully developed a basic local AI assistant with JSON-based persistent memory, keyword-based retrieval, and Ollama integration.

### Screenshots
