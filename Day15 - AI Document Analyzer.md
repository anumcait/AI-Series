# 🚀 Day 15 — AI Document Analyzer 📄

## Goal

Build a Python application that reads a business document and uses the Gemini API to extract structured, actionable information.

Analyzes the **entire document**.

## What We Will Extract

The AI will extract:

- Document type
- Requirements
- Roles
- Actions
- Dependencies
- Rules
- Exceptions
- Risks

## Project Flow

    Document
       ↓
    Read Text
       ↓
    Parameterized Prompt
       ↓
    Gemini
       ↓
    Structured JSON
       ↓
    Python JSON Validation

---

# 1. Project Structure

Create:

    Day-15/
    ├── document_analyzer.py
    └── purchase_process.txt

After running the application:

    document_analysis.json

will be created.

---

# 2. Install Dependencies

Activate your virtual environment:

    source ../../venv/Scripts/activate

Install:

    python -m pip install -U google-genai python-dotenv

Verify:

    python -c "from google import genai; print('google-genai works')"

    python -c "from dotenv import load_dotenv; print('python-dotenv works')"

---

# 3. Configure API Key

Create `.env`:

    GEMINI_API_KEY=your-api-key

---

# 4. requirements.txt

Create `requirements.txt`:

    google-genai
    python-dotenv

Install:

    python -m pip install -r requirements.txt

---

# 5. Create the Test Document

Create:

    purchase_process.txt

Use this ERP purchase process:

    ERP PURCHASE PROCESS

    Employees must create a purchase request in the ERP system.

    The request must contain:
    - Item or service description
    - Quantity
    - Estimated price
    - Required delivery date
    - Business justification
    - Cost center

    The purchase request must be approved by the employee's manager.

    Requests above $10,000 require approval from both the department
    manager and the finance department.

    After approval, the procurement team creates a purchase order.

    A purchase order must not be created before the required approvals
    are completed.

    When goods are delivered, the receiving team must record a goods
    receipt and verify the quantity and condition.

    If the delivered quantity differs from the purchase order, the
    difference must be reported to procurement.

    Damaged goods must be reported to procurement immediately.

    The accounts payable team must match the invoice against the
    purchase order and goods receipt.

    Payment must not be released if the invoice cannot be matched.

    Urgent purchases may bypass the normal process when authorized by
    the department manager and finance department.

    Incorrect purchase requests can result in incorrect orders.

    Missing approvals can create unauthorized purchases.

    Incorrect goods receipts can result in incorrect supplier payments.

    Invoice matching failures can result in payment errors or fraud.

---

# 6. Required JSON

Gemini must return:

    {
      "document_type": "",
      "requirements": [],
      "roles": [],
      "actions": [],
      "dependencies": [],
      "rules": [],
      "exceptions": [],
      "risks": []
    }

If a category does not exist in the document, return an empty array.

The AI must:

- Use only the supplied document.
- Not invent information.
- Preserve important numbers and conditions.
- Return only valid JSON.
- Not return Markdown or code fences.

---

# 7. Python Function

Create `document_analyzer.py`.

The main function must be:

    def analyze_document(document: str) -> str:
        ...

It should:

1. Load the Gemini API key.
2. Create a Gemini client.
3. Build a parameterized prompt.
4. Send the document to Gemini.
5. Get the response.
6. Remove accidental Markdown code fences.
7. Validate using `json.loads()`.
8. Check all required fields.
9. Return the JSON string.

---

# 8. Required Fields

Validate that these fields exist:

    document_type
    requirements
    roles
    actions
    dependencies
    rules
    exceptions
    risks

If Gemini returns invalid JSON, Python should raise:

    json.JSONDecodeError

Do not silently accept invalid AI output.

---

# 9. Read the Document Dynamically

Do not put the document directly inside the AI function.

Use:

    with open("purchase_process.txt", "r", encoding="utf-8") as file:
        document = file.read()

Then:

    result = analyze_document(document)

This means the same analyzer can later process:

    software_requirements.txt

or:

    incident_runbook.txt

without changing the AI logic.

---

# 10. Run

Execute:

    python document_analyzer.py

Expected flow:

    ============================================================
              DAY 15 - AI DOCUMENT ANALYZER
    ============================================================

    Reading document...
    Sending document to Gemini...

    Document Type:
    ERP Purchase Process

    Requirements:
    - Purchase requests must be created in the ERP system
    - Purchase requests must contain required information
    - ...

    Roles:
    - Employee
    - Manager
    - Procurement Team
    - ...

    Actions:
    - Create purchase request
    - Approve purchase request
    - Create purchase order
    - ...

    Analysis saved to:
    document_analysis.json

---

# 11. Example Output

The output should contain information similar to:

    {
      "document_type": "ERP Purchase Process",
      "requirements": [
        "Purchase requests must be created in the ERP system",
        "Purchase requests must contain required information"
      ],
      "roles": [
        "Employee",
        "Manager",
        "Procurement Team",
        "Receiving Team",
        "Accounts Payable Team"
      ],
      "actions": [
        "Create a purchase request",
        "Approve the purchase request",
        "Create a purchase order",
        "Record a goods receipt",
        "Verify the invoice"
      ],
      "dependencies": [
        "Purchase order creation depends on required approvals",
        "Invoice payment depends on successful invoice matching"
      ],
      "rules": [
        "Requests above $10,000 require additional approval",
        "Payment must not be released if invoice matching fails"
      ],
      "exceptions": [
        "Urgent purchases may bypass the normal process with authorization"
      ],
      "risks": [
        "Missing approvals can create unauthorized purchases",
        "Invoice matching failures can result in payment errors or fraud"
      ]
    }

The exact wording may differ because Gemini generates the response.

---

**Using AI to convert unstructured business documents into structured, machine-readable information.**

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/47f5253c-0d2d-4abd-9013-8847414e916a" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/68b71da2-4890-4365-b9f7-6dfd75d0b92e" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/7b7b8ac6-90ab-4c2f-9e10-5259d2937e49" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/73c3d849-efa0-4480-a91a-51509f4527d5" />





