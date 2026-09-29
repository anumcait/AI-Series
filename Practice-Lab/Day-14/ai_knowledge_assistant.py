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
        model="gemini-3.8-flash",
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
        # "When must remote employees use the VPN?",
        # "What are the standard working hours?",
        # "Where should employees report IT problems?",
        # "Does one day of sick leave require manager approval?",
        # "Can remote employees access internal applications without VPN?",
        # "What should an employee do if their company laptop is stolen?",
        # "What is the company's work-from-home internet reimbursement?",
        # "How many vacation days do employees receive?"
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
