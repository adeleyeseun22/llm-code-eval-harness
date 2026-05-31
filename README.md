# LLM Code Evaluation Harness

A Python evaluation harness for testing AI-generated code against benchmark tasks, unit tests, execution timeouts, and structured scoring reports.

This project demonstrates practical AI evaluation infrastructure, including benchmark loading, model submission evaluation, test execution, timeout handling, failure classification, and report generation.

---

## Why This Project Matters

Modern AI systems are often evaluated using benchmark tasks. For coding models, evaluation requires more than reading the generated code. The code must be executed against test cases, scored, and analyzed for failure patterns.

This project provides a lightweight Python-based evaluation harness that can test AI-generated code submissions against benchmark tasks and produce structured reports.

---

## Features

- Load benchmark coding tasks from JSON
- Load AI-generated code submissions from JSON
- Execute submitted Python code against task-specific tests
- Apply timeout protection for unsafe or infinite-running code
- Classify failure types
- Score submissions as pass or fail
- Generate JSON evaluation reports
- Generate CSV evaluation reports
- Provide a command-line interface
- Includes automated tests with `pytest`
- Uses a clean `src/` Python package structure

---

## Tech Stack

- Python
- Pydantic
- Typer
- Rich
- Pytest
- Ruff
- Mypy

---

## Project Structure

```text
llm-code-eval-harness/
│
├── benchmarks/
│   └── sample_tasks.json
│
├── submissions/
│   └── sample_submissions.json
│
├── reports/
│
├── src/
│   └── llm_code_eval_harness/
│       ├── __init__.py
│       ├── models.py
│       ├── loader.py
│       ├── evaluator.py
│       ├── report.py
│       └── cli.py
│
├── tests/
│   └── test_evaluator.py
│
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore