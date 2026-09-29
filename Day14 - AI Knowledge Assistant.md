# Day 14 - AI Knowledge Assistant

## AI Context-Aware Question Answering

Build a Python application that uses the Gemini API to answer questions from a **provided knowledge base** and return answers based only on the information contained in that context.

This project introduces **Context-Aware Question Answering**, **Prompt Grounding**, **Knowledge-Based AI**, and **Hallucination Reduction**.

The project is intentionally different from a generic chatbot. Instead of asking the AI to answer from its general knowledge, the application provides a specific company IT policy and requires the AI to answer **only from that information**.

## Objective

Build a Python-based **AI Knowledge Assistant** that:

1. Accepts a small company IT knowledge base.
2. Accepts a user question.
3. Sends the knowledge base and question to a Gemini AI model.
4. Answers the question using only the provided context.
5. Does not use outside knowledge.
6. Does not invent information that is missing.
7. Clearly indicates when the answer is not available.
8. Identifies the relevant policy section when possible.
9. Returns a structured JSON response.
10. Validates the JSON response using Python.

## Example Knowledge Base

    COMPANY IT POLICY

    LEAVE POLICY

    Employees are entitled to 18 casual leaves per calendar year.

    Leave requests must be submitted through the HR portal.

    Sick leave requires manager approval when the sick leave
    exceeds 2 consecutive working days.

    PASSWORD POLICY

    Employees must use passwords containing at least 12 characters.

    Passwords must contain uppercase letters, lowercase letters,
    numbers, and at least one special character.

    Employees must not share their passwords with other people.

    Passwords must be changed every 90 days.

    VPN POLICY

    Employees working remotely must connect to the company VPN
    when accessing internal company applications or systems.

    The company VPN must not be shared with unauthorized users.

    Employees should disconnect from the VPN when they finish
    accessing internal company systems.

    WORKING HOURS

    Standard working hours are Monday through Friday,
    9:00 AM to 6:00 PM.

    Employees are expected to be available during standard
    working hours unless they have an approved flexible-work
    arrangement.

    IT SUPPORT PROCESS

    Employees experiencing IT problems should create a support
    ticket through the company IT Service Desk portal.

    For critical issues that prevent business operations,
    employees may contact the IT Service Desk directly after
    creating the ticket.

    Employees should include a description of the problem,
    the affected application or device, and screenshots when
    available.

    LAPTOP AND SECURITY POLICY

    Company laptops must be protected with a password or
    approved biometric authentication.

    Employees must not install unauthorized software on
    company laptops.

    Company laptops must not be left unattended in public places.

    Employees must immediately report lost or stolen company
    devices to the IT Service Desk.

    Sensitive company information must not be stored on
    personal devices unless explicitly authorized by the company.

## Example Question

    How many casual leaves can an employee take?

## Expected Answer

    {
      "answer": "Employees are entitled to 18 casual leaves per calendar year.",
      "source": "Leave Policy",
      "found_in_context": true
    }

## Example Question

    Is manager approval required for one day of sick leave?

## Expected Answer

    {
      "answer": "According to the provided information, manager approval is required when sick leave exceeds 2 consecutive working days. Therefore, one day of sick leave does not require manager approval according to the provided policy.",
      "source": "Leave Policy",
      "found_in_context": true
    }

This example is important because the AI is required to **interpret the supplied information**, rather than simply copy a sentence from the knowledge base.

## Example Question

    When must a remote employee use the company VPN?

## Expected Answer

    {
      "answer": "Employees working remotely must connect to the company VPN when accessing internal company applications or systems.",
      "source": "VPN Policy",
      "found_in_context": true
    }

## Question Not Covered by the Knowledge Base

Ask:

    What is the company's work-from-home internet reimbursement?

The knowledge base does not contain this information.

The AI should return:

    {
      "answer": "The provided information does not contain the answer to this question.",
      "source": null,
      "found_in_context": false
    }

This is one of the most important parts of Day 14.

The AI should **not** invent an internet reimbursement amount.

## Required Output Schema

The application should always return:

    {
      "answer": null,
      "source": null,
      "found_in_context": false
    }

The fields are:

    answer
    source
    found_in_context

### `answer`

Contains the answer generated from the knowledge base.

### `source`

Contains the relevant policy section.

For example:

    Leave Policy
    Password Policy
    VPN Policy
    Working Hours
    IT Support Process
    Laptop and Security Policy

If the answer is not available:

    "source": null

### `found_in_context`

Indicates whether the answer was found in the supplied knowledge base.

    true

or:

    false

## Python File

Create a Python file named:

    knowledge_assistant.py

The application must contain:

    def answer_question(context: str, question: str) -> str:
        ...

## Requirements

- Use Python.
- Use the Gemini API.
- Use the `google-genai` SDK.
- Use `GEMINI_API_KEY` for the API key.
- Do not hardcode the API key.
- Pass the knowledge base dynamically into the prompt.
- Pass the user question dynamically into the prompt.
- Use a fixed JSON schema.
- Return only valid JSON.
- Do not use information outside the provided context.
- Return `null` when the answer is not present.
- Validate the response using `json.loads()`.

## Environment Setup

Activate the virtual environment:

    source ../../venv/Scripts/activate

Install the Gemini SDK:

    python -m pip install -U google-genai

Verify the installation:

    python -c "from google import genai; print('google-genai works')"

Set the API key:

    export GEMINI_API_KEY="your-api-key"

Verify:

    echo $GEMINI_API_KEY

Do not commit the API key to GitHub.

Add the following to `.gitignore`:

    .env
    venv/
    __pycache__/
    *.pyc

## Python Application

    import json
    import os

    from google import genai

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY")
    )

    def answer_question(context: str, question: str) -> str:

        prompt = f"""
    You are an AI Knowledge Assistant.

    Your job is to answer the user's question using ONLY the
    information contained in the provided knowledge base.

    Rules:

    1. Use only the provided knowledge base.
    2. Do not use outside knowledge.
    3. Do not make assumptions.
    4. Do not invent missing information.
    5. If the answer is not available in the knowledge base,
       return the required "information not available" response.
    6. If the question requires interpretation, reason only
       from the provided knowledge base.
    7. Keep the answer concise and factual.
    8. Identify the relevant policy section when possible.
    9. Return only valid JSON.
    10. Do not return Markdown.
    11. Do not return explanations outside the JSON.
    12. Use exactly the following JSON structure.

    {{
        "answer": null,
        "source": null,
        "found_in_context": false
    }}

    If the answer is available in the knowledge base:

    {{
        "answer": "answer based only on the provided context",
        "source": "relevant policy section",
        "found_in_context": true
    }}

    If the answer is not available:

    {{
        "answer": "The provided information does not contain the answer to this question.",
        "source": null,
        "found_in_context": false
    }}

    Knowledge Base:

    ------------------------------
    {context}
    ------------------------------

    User Question:

    {question}
    """

        response = client.models.generate_content(
            model="YOUR_AVAILABLE_GEMINI_MODEL",
            contents=prompt,
        )

        result = response.text.strip()

        # Remove Markdown code fences if the model returns them.
        if result.startswith("```json"):
            result = result[7:]

        if result.startswith("```"):
            result = result[3:]

        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()

        # Validate JSON
        json.loads(result)

        return result

    if __name__ == "__main__":

        knowledge_base = """
    COMPANY IT POLICY

    LEAVE POLICY

    Employees are entitled to 18 casual leaves per calendar year.

    Leave requests must be submitted through the HR portal.

    Sick leave requires manager approval when the sick leave
    exceeds 2 consecutive working days.

    PASSWORD POLICY

    Employees must use passwords containing at least 12 characters.

    Passwords must contain uppercase letters, lowercase letters,
    numbers, and at least one special character.

    Employees must not share their passwords with other people.

    Passwords must be changed every 90 days.

    VPN POLICY

    Employees working remotely must connect to the company VPN
    when accessing internal company applications or systems.

    The company VPN must not be shared with unauthorized users.

    WORKING HOURS

    Standard working hours are Monday through Friday,
    9:00 AM to 6:00 PM.

    IT SUPPORT PROCESS

    Employees experiencing IT problems should create a support
    ticket through the company IT Service Desk portal.

    For critical issues that prevent business operations,
    employees may contact the IT Service Desk directly after
    creating the ticket.

    LAPTOP AND SECURITY POLICY

    Company laptops must be protected with a password or
    approved biometric authentication.

    Employees must not install unauthorized software on
    company laptops.

    Employees must immediately report lost or stolen company
    devices to the IT Service Desk.
    """

        questions = [
            "How many casual leaves can an employee take?",
            "How long must a company password be?",
            "When must remote employees use the VPN?",
            "What are the standard working hours?",
            "Where should employees report IT problems?",
            "Does one day of sick leave require manager approval?",
            "Can remote employees access internal applications without VPN?",
            "What should an employee do if their company laptop is stolen?",
            "What is the company's work-from-home internet reimbursement?",
            "How many vacation days do employees receive?"
        ]

        for question in questions:

            print("\n" + "=" * 60)
            print("QUESTION:")
            print(question)

            try:

                result = answer_question(
                    knowledge_base,
                    question
                )

                print("\nAI RESPONSE:")
                print(result)

            except json.JSONDecodeError:

                print("\nERROR:")
                print("Gemini returned invalid JSON.")

            except Exception as error:

                print("\nERROR:")
                print(error)

## Running the Application

Run:

    python knowledge_assistant.py

The application will test multiple questions.

Example:

    ============================================================
    QUESTION:
    How many casual leaves can an employee take?

    AI RESPONSE:
    {
      "answer": "Employees are entitled to 18 casual leaves per calendar year.",
      "source": "Leave Policy",
      "found_in_context": true
    }

Another example:

    ============================================================
    QUESTION:
    What is the company's work-from-home internet reimbursement?

    AI RESPONSE:
    {
      "answer": "The provided information does not contain the answer to this question.",
      "source": null,
      "found_in_context": false
    }

## Interactive Version

After completing the basic implementation, modify the application so that the user can continuously ask questions.

Add:

    def run_assistant(context: str):

        print("=" * 60)
        print("       DAY 14 - AI KNOWLEDGE ASSISTANT")
        print("=" * 60)

        print("\nAsk questions about the company IT policy.")
        print("Type 'exit' to quit.\n")

        while True:

            question = input("You: ").strip()

            if question.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if not question:
                print("Please enter a question.")
                continue

            try:

                result = answer_question(
                    context,
                    question
                )

                print("\nAI:")
                print(result)

            except json.JSONDecodeError:

                print("\nAI returned invalid JSON.")

            except Exception as error:

                print("\nError:")
                print(error)

Then call:

    run_assistant(knowledge_base)

## Interactive Example

    ============================================================
           DAY 14 - AI KNOWLEDGE ASSISTANT
    ============================================================

    Ask questions about the company IT policy.
    Type 'exit' to quit.

    You: How many casual leaves can I take?

    AI:
    {
      "answer": "Employees are entitled to 18 casual leaves per calendar year.",
      "source": "Leave Policy",
      "found_in_context": true
    }

    You: Can I share my password with my teammate?

    AI:
    {
      "answer": "No. Employees must not share their passwords with other people.",
      "source": "Password Policy",
      "found_in_context": true
    }

    You: How much internet reimbursement do I get?

    AI:
    {
      "answer": "The provided information does not contain the answer to this question.",
      "source": null,
      "found_in_context": false
    }

    You: exit

    Goodbye!

## Question Categories

The Day 14 lab should test three different types of questions.

### 1. Direct Questions

The answer is explicitly present.

Example:

    How many casual leaves can employees take?

The knowledge base directly says:

    18 casual leaves per calendar year.

### 2. Interpretation Questions

The answer requires reasoning over information in the context.

Example:

    Does one day of sick leave require manager approval?

The context says:

    Manager approval is required when sick leave exceeds
    2 consecutive working days.

The AI needs to interpret the condition.

### 3. Missing Information

The answer does not exist in the knowledge base.

Example:

    What is the company's work-from-home internet allowance?

The correct behavior is:

    The provided information does not contain the answer
    to this question.

This third category is particularly important for understanding **hallucination control**.

## Lab Challenge

Create at least **10 different questions**.

### 5 Questions That Can Be Answered Directly

    1. How many casual leaves are available?
    2. What is the minimum password length?
    3. When must employees use the VPN?
    4. What are the standard working hours?
    5. Where should IT problems be reported?

### 3 Questions Requiring Interpretation

    6. Does one day of sick leave require manager approval?
    7. Can a remote employee access internal systems without VPN?
    8. What should an employee do after losing their company laptop?

### 2 Questions Where the Information Does Not Exist

    9. How much internet reimbursement does the company provide?
    10. How many annual vacation days does an employee receive?

## Additional Challenge

Create a second knowledge base containing:

    HR Policy
    Finance Policy
    Security Policy
    Travel Policy
    Remote Work Policy

Then test whether the AI answers only from the supplied knowledge base.

For example, if the context contains:

    Employees may work remotely two days per week.

Ask:

    How many days can employees work remotely?

The answer should be:

    Employees may work remotely two days per week.

But if you ask:

    Can employees work remotely from another country?

and that information isn't provided, the AI should not invent a policy.

## JSON Validation

The application uses:

    json.loads(result)

to validate the Gemini response.

For example:

    result = json.loads(response.text)

If Gemini returns valid JSON:

    Valid JSON
        ↓
    Python dictionary

If Gemini returns invalid JSON:

    Invalid JSON
        ↓
    JSONDecodeError

This is important because an AI response should not automatically be trusted as application-ready data.

## Why JSON Validation Matters

Consider this response:

    Employees receive 18 casual leaves per year.

This is useful for a human but isn't necessarily structured data.

Compare that with:

    {
      "answer": "Employees receive 18 casual leaves per year.",
      "source": "Leave Policy",
      "found_in_context": true
    }

Now Python can process it:

    data = json.loads(result)

    print(data["answer"])
    print(data["source"])
    print(data["found_in_context"])

This makes the output usable by:

- APIs
- Databases
- Web applications
- Automation workflows
- ERP systems
- IT service management systems
- Reporting pipelines

## Project Flow

    Knowledge Base
            ↓
    User Question
            ↓
    Python Application
            ↓
    Parameterized Prompt
            ↓
    Gemini API
            ↓
    Context-Based Reasoning
            ↓
    Structured JSON
            ↓
    Python JSON Validation
            ↓
    Answer + Source

## AI Grounding Concept

Introduces an important concept:

    General AI Question
            ↓
    "Answer using what you know"

versus:

    Grounded AI Question
            ↓
    "Answer using ONLY this information"

The second approach is particularly useful for enterprise applications where answers should be based on controlled business information.

## Architecture

                     ┌──────────────────────┐
                     │   Company Policies   │
                     │                      │
                     │ Leave                │
                     │ Password             │
                     │ VPN                  │
                     │ Working Hours        │
                     │ IT Support           │
                     │ Security             │
                     └──────────┬───────────┘
                                │
                                ↓
                     ┌──────────────────────┐
                     │   User Question      │
                     └──────────┬───────────┘
                                │
                                ↓
                     ┌──────────────────────┐
                     │ Prompt Engineering   │
                     │                      │
                     │ Context + Question   │
                     └──────────┬───────────┘
                                │
                                ↓
                     ┌──────────────────────┐
                     │     Gemini API       │
                     │                      │
                     │   Gemini Flash       │
                     └──────────┬───────────┘
                                │
                                ↓
                     ┌──────────────────────┐
                     │   Structured JSON    │
                     │                      │
                     │ Answer               │
                     │ Source               │
                     │ Found in Context     │
                     └──────────┬───────────┘
                                │
                                ↓
                     ┌──────────────────────┐
                     │    JSON Validation   │
                     │      json.loads()    │
                     └──────────────────────┘


### Screenshots

<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/9450f6c1-3cbf-44f8-a899-951213e793cc" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/f5d44283-2964-4886-aba0-97d62855e008" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/8fd2ae39-bd9d-4db8-b75a-fb3e81522fdb" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/7e12adca-3194-4a14-91ec-1bda5c40887a" />




