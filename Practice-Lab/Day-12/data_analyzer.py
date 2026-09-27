import json
import os

from google import genai


client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


def analyze_data(data: str) -> str:
    prompt = f"""
Analyze the following employee dataset.

Calculate:
1. Total number of employees.
2. Employee with the highest salary.
3. Average salary.
4. Unique departments.
5. Average experience.

Return only valid JSON using exactly these fields:

{{
    "total_employees": number,
    "highest_salary_employee": "name",
    "average_salary": number,
    "departments": ["department"],
    "average_experience": number
}}

Do not add any additional fields.

Employee dataset:

{data}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    return response.text.strip()


if __name__ == "__main__":
    data = """Employee, Department, Salary, Experience
Rahul, IT, 85000, 5
Priya, HR, 65000, 4
Arun, IT, 95000, 7
Sneha, Finance, 72000, 6"""

    response = analyze_data(data)

    print(response)