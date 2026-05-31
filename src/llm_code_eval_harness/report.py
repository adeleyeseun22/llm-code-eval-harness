import csv
import json
from pathlib import Path
from typing import Any

from llm_code_eval_harness.models import EvaluationResult, EvaluationSummary


def model_to_dict(model: EvaluationSummary | EvaluationResult) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()

    return model.dict()


def save_json_report(summary: EvaluationSummary, output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(model_to_dict(summary), indent=2),
        encoding="utf-8",
    )


def save_csv_report(results: list[EvaluationResult], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "task_id",
        "title",
        "model_name",
        "passed",
        "score",
        "runtime_ms",
        "error_type",
        "error_message",
    ]

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            row = model_to_dict(result)
            writer.writerow({field: row.get(field) for field in fieldnames})


def format_console_summary(summary: EvaluationSummary) -> str:
    return f"""
LLM CODE EVALUATION SUMMARY
===========================

Total submissions: {summary.total_submissions}
Passed submissions: {summary.passed_submissions}
Failed submissions: {summary.failed_submissions}

Pass rate: {summary.pass_rate}%
Average score: {summary.average_score}
""".strip()