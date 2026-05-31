import subprocess
import sys
import tempfile
import time
from pathlib import Path

from llm_code_eval_harness.models import (
    BenchmarkTask,
    CodeSubmission,
    EvaluationResult,
    EvaluationSummary,
)


def build_test_script(task: BenchmarkTask, submission: CodeSubmission) -> str:
    test_block = "\n".join(task.tests)

    return f"""
{submission.code}

{test_block}
""".strip()


def classify_error(stderr: str, return_code: int) -> str | None:
    if return_code == 0:
        return None

    if "AssertionError" in stderr:
        return "assertion_error"

    if "SyntaxError" in stderr:
        return "syntax_error"

    if "NameError" in stderr:
        return "name_error"

    if "TypeError" in stderr:
        return "type_error"

    return "runtime_error"


def evaluate_submission(
    task: BenchmarkTask,
    submission: CodeSubmission,
) -> EvaluationResult:
    script_content = build_test_script(task, submission)
    start_time = time.perf_counter()

    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = Path(temp_dir) / "candidate_solution.py"
        script_path.write_text(script_content, encoding="utf-8")

        try:
            completed_process = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=task.timeout_seconds,
                check=False,
            )

            runtime_ms = round((time.perf_counter() - start_time) * 1000, 2)
            passed = completed_process.returncode == 0

            error_type = classify_error(
                completed_process.stderr,
                completed_process.returncode,
            )

            error_message = (
                completed_process.stderr.strip()
                if completed_process.stderr.strip()
                else None
            )

            return EvaluationResult(
                task_id=task.task_id,
                title=task.title,
                model_name=submission.model_name,
                passed=passed,
                score=1.0 if passed else 0.0,
                runtime_ms=runtime_ms,
                error_type=error_type,
                error_message=error_message,
                stdout=completed_process.stdout.strip(),
                stderr=completed_process.stderr.strip(),
            )

        except subprocess.TimeoutExpired as error:
            runtime_ms = round((time.perf_counter() - start_time) * 1000, 2)

            return EvaluationResult(
                task_id=task.task_id,
                title=task.title,
                model_name=submission.model_name,
                passed=False,
                score=0.0,
                runtime_ms=runtime_ms,
                error_type="timeout",
                error_message=f"Execution exceeded {task.timeout_seconds} seconds.",
                stdout=error.stdout.decode("utf-8") if isinstance(error.stdout, bytes) else "",
                stderr=error.stderr.decode("utf-8") if isinstance(error.stderr, bytes) else "",
            )


def evaluate_all(
    tasks: list[BenchmarkTask],
    submissions: list[CodeSubmission],
) -> EvaluationSummary:
    task_lookup = {task.task_id: task for task in tasks}
    results: list[EvaluationResult] = []

    for submission in submissions:
        task = task_lookup.get(submission.task_id)

        if task is None:
            results.append(
                EvaluationResult(
                    task_id=submission.task_id,
                    title="Unknown task",
                    model_name=submission.model_name,
                    passed=False,
                    score=0.0,
                    runtime_ms=0.0,
                    error_type="missing_benchmark_task",
                    error_message="No matching benchmark task was found for this submission.",
                )
            )
            continue

        results.append(evaluate_submission(task, submission))

    total_submissions = len(results)
    passed_submissions = sum(result.passed for result in results)
    failed_submissions = total_submissions - passed_submissions

    pass_rate = (
        round((passed_submissions / total_submissions) * 100, 2)
        if total_submissions > 0
        else 0.0
    )

    average_score = (
        round(sum(result.score for result in results) / total_submissions, 3)
        if total_submissions > 0
        else 0.0
    )

    return EvaluationSummary(
        total_submissions=total_submissions,
        passed_submissions=passed_submissions,
        failed_submissions=failed_submissions,
        pass_rate=pass_rate,
        average_score=average_score,
        results=results,
    )