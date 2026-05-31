import json
from pathlib import Path
from typing import Any

from llm_code_eval_harness.models import BenchmarkTask, CodeSubmission


def load_json_file(file_path: str | Path) -> list[dict[str, Any]]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() != ".json":
        raise ValueError("Only JSON files are supported.")

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError("JSON file must contain a list of records.")

    return data


def load_benchmark_tasks(file_path: str | Path) -> list[BenchmarkTask]:
    records = load_json_file(file_path)
    return [BenchmarkTask(**record) for record in records]


def load_code_submissions(file_path: str | Path) -> list[CodeSubmission]:
    records = load_json_file(file_path)
    return [CodeSubmission(**record) for record in records]