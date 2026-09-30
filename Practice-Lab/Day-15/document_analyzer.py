import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Please add it to your .env file."
    )


client = genai.Client(api_key=api_key)


# ---------------------------------------------------------
# Document Analyzer
# ---------------------------------------------------------

def analyze_document(document: str) -> str:
    """
    Analyze a business document using Gemini.

    Returns:
        str: Structured JSON containing the document analysis.
    """

    prompt = f"""
You are an expert business document analyzer.

Your task is to analyze the provided business document and
extract important actionable information.

Use ONLY the information contained in the supplied document.

Do not use outside knowledge.

Do not invent facts.

Extract the following information:

1. document_type
   - Identify the type of document.

2. requirements
   - Extract mandatory requirements.

3. roles
   - Identify people, teams, or departments responsible
     for activities.

4. actions
   - Extract actions that must be performed.

5. dependencies
   - Identify things that must happen before another
     action or process step can happen.

6. rules
   - Extract policies, restrictions, thresholds,
     conditions, and mandatory rules.

7. exceptions
   - Identify situations where the normal process
     changes or can be bypassed.

8. risks
   - Extract explicitly mentioned risks, warnings,
     consequences, financial risks, security risks,
     or operational risks.

Important rules:

- Use only the provided document.
- Do not invent information.
- Do not make assumptions.
- Preserve important numbers and conditions.
- Keep each item concise.
- If a category has no information, return an empty array.
- Return ONLY valid JSON.
- Do not return Markdown.
- Do not return code fences.
- Do not add explanations outside the JSON.

Return exactly this JSON structure:

{{
    "document_type": "",
    "requirements": [],
    "roles": [],
    "actions": [],
    "dependencies": [],
    "rules": [],
    "exceptions": [],
    "risks": []
}}

DOCUMENT
========

{document}

========

Analyze the document and return the JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json"
        )
    )

    result = response.text.strip()

    # -----------------------------------------------------
    # Remove Markdown code fences if Gemini returns them
    # -----------------------------------------------------

    if result.startswith("```json"):
        result = result[7:]

    elif result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    # -----------------------------------------------------
    # Validate JSON
    # -----------------------------------------------------

    try:
        parsed_result = json.loads(result)

    except json.JSONDecodeError as error:
        print("\nGemini returned invalid JSON:")
        print(result)

        raise ValueError(
            "Gemini returned invalid JSON."
        ) from error

    # -----------------------------------------------------
    # Validate required fields
    # -----------------------------------------------------

    required_fields = [
        "document_type",
        "requirements",
        "roles",
        "actions",
        "dependencies",
        "rules",
        "exceptions",
        "risks"
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in parsed_result
    ]

    if missing_fields:
        raise ValueError(
            f"Missing required JSON fields: {missing_fields}"
        )

    # Return normalized JSON
    return json.dumps(
        parsed_result,
        indent=2,
        ensure_ascii=False
    )


# ---------------------------------------------------------
# Read Document
# ---------------------------------------------------------

def read_document(file_path: str) -> str:
    """
    Read a text document from disk.
    """

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except FileNotFoundError as error:

        raise FileNotFoundError(
            f"Document not found: {file_path}"
        ) from error


# ---------------------------------------------------------
# Display Analysis
# ---------------------------------------------------------

def print_analysis(result: str):
    """
    Display structured analysis in a readable format.
    """

    data = json.loads(result)

    print("\n" + "=" * 70)
    print("              AI DOCUMENT ANALYZER")
    print("=" * 70)

    print("\nDOCUMENT TYPE")
    print("-" * 70)
    print(data["document_type"])

    print("\nREQUIREMENTS")
    print("-" * 70)

    for item in data["requirements"]:
        print(f"- {item}")

    print("\nROLES")
    print("-" * 70)

    for item in data["roles"]:
        print(f"- {item}")

    print("\nACTIONS")
    print("-" * 70)

    for item in data["actions"]:
        print(f"- {item}")

    print("\nDEPENDENCIES")
    print("-" * 70)

    for item in data["dependencies"]:
        print(f"- {item}")

    print("\nRULES")
    print("-" * 70)

    for item in data["rules"]:
        print(f"- {item}")

    print("\nEXCEPTIONS")
    print("-" * 70)

    for item in data["exceptions"]:
        print(f"- {item}")

    print("\nRISKS")
    print("-" * 70)

    for item in data["risks"]:
        print(f"- {item}")

    print("\n" + "=" * 70)


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("           DAY 15 - AI DOCUMENT ANALYZER")
    print("=" * 70)

    document_path = "purchase_process.txt"

    try:

        # Read document
        print("\nReading document...")

        document = read_document(
            document_path
        )

        if not document.strip():
            raise ValueError(
                "The document is empty."
            )

        print(
            f"Document loaded successfully: "
            f"{document_path}"
        )

        # Analyze document
        print("\nSending document to Gemini...")
        print("Please wait...")

        result = analyze_document(
            document
        )

        # Display result
        print_analysis(
            result
        )

        # Save JSON output
        output_file = "document_analysis.json"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(result)

        print(
            f"\nJSON analysis saved to: "
            f"{output_file}"
        )

    except Exception as error:

        print("\n" + "=" * 70)
        print("ERROR")
        print("=" * 70)

        print(error)