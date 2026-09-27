# Day 12 - AI Data Analyzer

## AI Data Analyzer

The AI Engineering team wants to use AI to analyze small datasets and return useful business insights in a structured format.

The task is to build a python application that sends employee data to an AI model and ask it to calculate summary information.

It introduces **Structured AI Output** and basic data analysis.

## Objective
Build a Python-based **AI Data Analyzer** that:

1. Accepts a small employee dataset.
2. Sends the dataset to an AI model.
3. Calculates the total number of employees.
4. Identifies the employee with the highest salary.
5. Calculates the average salary.
6. Identifies the departments.
7. Calculates the average experience.
8. Returns the result as structured JSON.

---

## Dataset

Use the following employee dataset:

```text
Employee, Department, Salary, Experience
Rahul, IT, 85000, 5
Priya, HR, 65000, 4
Arun, IT, 95000, 7
Sneha, Finance, 72000, 6
```
---

## Required Output

The AI should return information using this JSON structure:

```json
{
  "total_employees": 4,
  "highest_salary_employee": "Arun",
  "average_salary": 79250,
  "departments": ["IT", "HR", "Finance"],
  "average_experience": 5.5
}
```
The values should be calculated from the supplied dataset.

---

## Function

Create a Python file named:

```text
data_analyzer.py
```

The application must contain:

```python
def analyze_data(data: str) -> str:
    ...

```

The function must accept the employee dataset dynamically.

---

## Input

Use this dataset for the first test:

```text
Employee, Department, Salary, Experience
Rahul, IT, 85000, 5
Priya, HR, 65000, 4
Arun, IT, 95000, 7
Sneha, Finance, 72000, 6
```

---

## Expected Output

Return valid JSON with exactly these fields:

```json
{
  "total_employees": 4,
  "highest_salary_employee": "Arun",
  "average_salary": 79250,
  "departments": ["IT", "HR", "Finance"],
  "average_experience": 5.5
}
```

---

## Requirements

- Use Python.
- Use the Gemini API.
- Use `GEMINI_API_KEY` for the API key.
- Do not hardcode the API key.
- Create a Gemini client.
- Create `analyze_data(data)`.
- Pass the dataset dynamically into the prompt.
- Return only valid JSON.
- Print the final result.

---

## Environment Setup

If your existing `venv` is outside the `Practice-Lab` directory, activate it from `Day-12`.

```bash
source ../../venv/Scripts/activate
```

Install the Gemini SDK:

```bash
python -m pip install -U google-genai
```

Verify:

```bash
python -c "from google import genai; print('google-genai works')"
```

Set the API key:

```bash
export GEMINI_API_KEY="your-api-key"
```

---

## Python Structure

```python
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

Employee dataset:

{data}
"""

    response = client.models.generate_content(
        model="YOUR_AVAILABLE_GEMINI_MODEL",
        contents=prompt,
    )

    return response.text.strip()


if __name__ == "__main__":
    data = """Employee, Department, Salary, Experience
Rahul, IT, 85000, 5
Priya, HR, 65000, 4
Arun, IT, 95000, 7
Sneha, Finance, 72000, 6"""

    print(analyze_data(data))
```

Replace `YOUR_AVAILABLE_GEMINI_MODEL` with a currently available Gemini model.

---

## Test Cases

### Test Case 1

Use the provided dataset and verify:

```text
Employees: 4
Highest Salary: Arun
Average Salary: 79250
Departments: IT, HR, Finance
Average Experience: 5.5
```

### Test Case 2

Try another dataset:

```text
Employee, Department, Salary, Experience
Amit, IT, 70000, 3
Ravi, HR, 60000, 4
Neha, Finance, 90000, 6
```

Check whether the AI calculates the values correctly.

---

## Troubleshooting

If you get:

```text
ImportError: cannot import name 'genai' from 'google'
```

Activate the correct virtual environment:

```bash
source ../../venv/Scripts/activate
```

Then install:

```bash
python -m pip install -U google-genai
```

Check Python:

```bash
python -c "import sys; print(sys.executable)"
```

If you get a `404 NOT_FOUND` error, check whether the selected Gemini model is currently available.

---

## Run the Application

```bash
cd Day-12
source ../../venv/Scripts/activate
python data_analyzer.py
```

---

You should gain experience with:

- Python functions
- Virtual environments
- Environment variables
- Gemini API
- Prompt engineering
- Dynamic data
- JSON output
- AI-powered data analysis
- Basic troubleshooting

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/49492318-fe79-4d95-83e3-16f2e0047a9a" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/39898c76-8921-4558-89a7-3451406ee2a5" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/f45e7730-5f13-42ef-ab49-5b60d0a42008" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/1717a79e-0d2c-4f85-96dd-cb3f953e9e4d" />




