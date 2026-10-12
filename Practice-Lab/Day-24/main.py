from ollama import chat

# The model installed through Ollama.
MODEL_NAME = "llama3.2:3b"

# Maximum number of conversation messages retained.
# Ten messages means up to five user/assistant exchanges.
MAX_HISTORY_MESSAGES = 10

SYSTEM_PROMPT = """
You are a helpful local AI assistant.

Use the conversation history to understand follow-up questions.
When discussing a technical issue, refer to earlier details when relevant.
Do not invent facts that the user has not provided.
If important context is missing, ask a clarifying question.
Explain technical recommendations clearly and safely.
"""


# Short-term memory: exists only while this program is running.
conversation_history = []


def trim_history():
    """
    Keep only the most recent complete user/assistant exchanges.

    We remove two messages at a time so that we do not deliberately
    retain an incomplete pair when trimming the history.
    """
    while len(conversation_history) > MAX_HISTORY_MESSAGES:
        del conversation_history[:2]


def show_memory():
    """Display the messages currently stored in memory."""
    print("\n--- Conversation Memory ---")

    if not conversation_history:
        print("Memory is empty.")
        return

    for index, message in enumerate(conversation_history, start=1):
        role = message["role"].upper()
        content = message["content"]

        print(f"{index}. {role}: {content}")

    print(
        f"\nStored messages: {len(conversation_history)}"
        f" / {MAX_HISTORY_MESSAGES}"
    )
    print("---------------------------\n")


def reset_memory():
    """Clear all user and assistant messages from this session."""
    conversation_history.clear()
    print("Conversation memory has been reset.\n")


def get_response(user_input):
    """
    Send the current conversation context to Ollama
    and return the assistant's response.
    """

    # Build the request without modifying stored history yet.
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *conversation_history,
        {"role": "user", "content": user_input},
    ]

    # Ollama receives earlier messages along with the new question.
    response = chat(
        model=MODEL_NAME,
        messages=messages,
    )

    assistant_reply = response.message.content

    # Save the exchange only after Ollama returns successfully.
    conversation_history.append(
        {"role": "user", "content": user_input}
    )
    conversation_history.append(
        {"role": "assistant", "content": assistant_reply}
    )

    # Enforce the memory limit after each successful exchange.
    trim_history()

    return assistant_reply


def main():
    print("=" * 55)
    print("Day 24 - Local AI Agent with Short-Term Memory")
    print(f"Model: {MODEL_NAME}")
    print("=" * 55)

    print("Commands: /help, /memory, /reset, /exit")
    print("Ask a question to start the conversation.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            # Ignore blank messages.
            if not user_input:
                continue

            command = user_input.lower()

            if command == "/exit":
                print("Goodbye!")
                break

            elif command == "/help":
                print(
                    "\nAvailable commands:\n"
                    "  /help   - Show available commands\n"
                    "  /memory - Inspect stored conversation history\n"
                    "  /reset  - Clear conversation memory\n"
                    "  /exit   - Exit the application\n"
                )
                continue

            elif command == "/memory":
                show_memory()
                continue

            elif command == "/reset":
                reset_memory()
                continue

            # Send normal messages to the model.
            try:
                reply = get_response(user_input)
                print(f"\nAssistant: {reply}\n")

            except Exception as error:
                print("\nCould not get a response from Ollama.")
                print(f"Details: {error}")
                print(
                    "Check that Ollama is running and that "
                    f"the model '{MODEL_NAME}' is installed.\n"
                )

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()