# Day 13 - AI Entity Extraction

## AI Incident Entity Extractor

Build a Python application that uses the Gemini API to extract important operational entities from an unstructured IT incident description and return them as structured JSON.

This project introduces **Information Extraction**, **Schema-Based Prompting**, and **Structured AI Output**.

## Objective

Build a Python-based **AI Incident Entity Extractor** that:

1. Accepts an unstructured IT incident description.
2. Sends the incident description to a Gemini AI model.
3. Extracts predefined operational entities.
4. Maps the extracted information to a fixed JSON schema.
5. Handles missing entities using `null`.
6. Returns valid JSON.
7. Validates the JSON response using Python.

## Example Input

```text
The production payment API started returning 503 errors
in the AWS Mumbai region at 10:30 AM. The issue affected
the ECS payment service and approximately 200 users.
The incident was classified as high severity.
```

## Required Entities

```text
environment
service
cloud
region
platform
component
error
error_type
start_time
affected_users
severity
issue
trigger
```

## Expected Output

```json
{
  "environment": "Production",
  "service": "Payment API",
  "cloud": "AWS",
  "region": "Mumbai",
  "platform": "ECS",
  "component": null,
  "error": "503",
  "error_type": "Service Unavailable",
  "start_time": "10:30 AM",
  "affected_users": 200,
  "severity": "High",
  "issue": "Payment API returning 503 errors",
  "trigger": null
}
```

If an entity is not present in the incident, return `null`.

## Python File

Create a Python file named:

```text
incident_entity_extractor.py
```

The application must contain:

```python
def extract_incident_entities(incident: str) -> str:
    ...
```

## Requirements

- Use Python.
- Use the Gemini API.
- Use the `google-genai` SDK.
- Use `GEMINI_API_KEY` for the API key.
- Do not hardcode the API key.
- Pass the incident dynamically into the prompt.
- Use a fixed JSON schema.
- Return only valid JSON.
- Use `null` for missing entities.
- Validate the response using `json.loads()`.

## Environment Setup

Activate the virtual environment:

```bash
source ../../venv/Scripts/activate
```

Install the Gemini SDK:

```bash
python -m pip install -U google-genai
```

Verify the installation:

```bash
python -c "from google import genai; print('google-genai works')"
```

Set the API key:

```bash
export GEMINI_API_KEY="your-api-key"
```

Verify:

```bash
echo $GEMINI_API_KEY
```

Do not commit the API key to GitHub.

## Python Application

```python
import json
import os

from google import genai


client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


def extract_incident_entities(incident: str) -> str:

    prompt = f"""
You are an AI incident analysis assistant.

Extract the following operational entities from the incident:

- environment
- service
- cloud
- region
- platform
- component
- error
- error_type
- start_time
- affected_users
- severity
- issue
- trigger

Rules:

1. Extract only information explicitly mentioned or clearly stated.
2. Do not invent information.
3. If an entity is not present, return null.
4. Preserve technical values such as HTTP error codes.
5. Normalize severity to Low, Medium, High, or Critical.
6. Return only valid JSON.
7. Do not return Markdown.
8. Do not include explanations.
9. Use exactly the following JSON structure.

{{
    "environment": null,
    "service": null,
    "cloud": null,
    "region": null,
    "platform": null,
    "component": null,
    "error": null,
    "error_type": null,
    "start_time": null,
    "affected_users": null,
    "severity": null,
    "issue": null,
    "trigger": null
}}

Incident description:

{incident}
"""

    response = client.models.generate_content(
        model="YOUR_AVAILABLE_GEMINI_MODEL",
        contents=prompt,
    )

    result = response.text.strip()

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

    incident = """
The production payment API started returning 503 errors
in the AWS Mumbai region at 10:30 AM. The issue affected
the ECS payment service and approximately 200 users.
The incident was classified as high severity.
"""

    print(extract_incident_entities(incident))
```

Replace:

```text
YOUR_AVAILABLE_GEMINI_MODEL
```

with a currently available Gemini model.

## Incident Examples

### Staging Web Application

```text
The staging web application is returning 502 errors
from the ALB. The issue started at 3:15 PM and is affecting
the frontend service.
```

Expected entities include:

```text
environment: Staging
service: Frontend
component: ALB
error: 502
start_time: 3:15 PM
```

### Database Incident

```text
The production database connection pool was exhausted
after a sudden increase in traffic. The application is
running on ECS in the Hyderabad environment.
```

Expected entities include:

```text
environment: Production
platform: ECS
region: Hyderabad
component: Database
issue: Connection pool exhausted
trigger: Increase in traffic
```

### Kubernetes Incident

```text
The production order service running on Kubernetes
started returning HTTP 500 errors at 11:45 AM.
The incident affected approximately 75 customers.
Severity was classified as Critical.
```

Expected entities include:

```text
environment: Production
service: Order Service
platform: Kubernetes
error: 500
start_time: 11:45 AM
affected_users: 75
severity: Critical
```

## Lab Challenge

Create at least **5 different IT incident descriptions**.

For each incident:

- Include different services and errors.
- Leave some entities missing.
- Verify missing entities return `null`.
- Verify the AI does not invent information.
- Verify the response is valid JSON.

## JSON Validation

The application uses:

```python
json.loads(result)
```

to verify that the AI response is valid JSON.

This is important because AI-generated responses should be validated before being passed to another application or database.

## Project Flow

```text
Incident Description
        ↓
Python Application
        ↓
Gemini API
        ↓
Entity Extraction
        ↓
Predefined Schema
        ↓
Structured JSON
        ↓
Python JSON Validation
```

## What You Will Learn

- Information extraction
- Entity extraction
- Schema-based prompting
- Structured JSON output
- Handling missing entities
- JSON validation
- Gemini API
- Python environment variables
- AI-powered DevOps incident processing

### Screenshots
