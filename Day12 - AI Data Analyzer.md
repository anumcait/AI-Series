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
