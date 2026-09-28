import json
import os

from google import genai


client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


def extract_incident_entities(incident: str) -> str:
    prompt = f"""
You are an AI incident analysis assistant.

Extract specific operational entities from the incident description below.

The required entities are:

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

1. Extract only information explicitly mentioned or clearly stated in the incident.
2. Do not invent information.
3. If an entity is not present, return null.
4. Preserve important values such as error codes exactly.
5. Normalize severity to one of:
   "Low", "Medium", "High", "Critical"
   when severity is explicitly provided.
6. Return only valid JSON.
7. Do not include Markdown.
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

    # Validate that the response is valid JSON.
    json.loads(result)

    return result


if __name__ == "__main__":

    incident = """
The production payment API started returning 503 errors
in the AWS Mumbai region at 10:30 AM. The issue affected
the ECS payment service and approximately 200 users.
The incident was classified as high severity.
"""

    result = extract_incident_entities(incident)

    print(result)
