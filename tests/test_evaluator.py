from llm_code_eval_harness.evaluator import evaluate_all, evaluate_submission
from llm_code_eval_harness.models import BenchmarkTask, CodeSubmission


def test_correct_submission_passes() -> None:
    task = BenchmarkTask(
        task_id="sum_two_numbers",
        title="Sum Two Numbers",
        prompt="Write add_numbers.",
        entrypoint="add_numbers",
        tests=[
            "assert add_numbers(2, 3) == 5",
            "assert add_numbers(-1, 1) == 0",
        ],
        timeout_seconds=2,
    )

    submission = CodeSubmission(
        task_id="sum_two_numbers",
        model_name="model_alpha",
        code="def add_numbers(a, b):\n    return a + b\n",
    )

    result = evaluate_submission(task, submission)

    assert result.passed is True
    assert result.score == 1.0
    assert result.error_type is None


def test_incorrect_submission_fails() -> None:
    task = BenchmarkTask(
        task_id="sum_two_numbers",
        title="Sum Two Numbers",
        prompt="Write add_numbers.",
        entrypoint="add_numbers",
        tests=[
            "assert add_numbers(2, 3) == 5",
        ],
        timeout_seconds=2,
    )

    submission = CodeSubmission(
        task_id="sum_two_numbers",
        model_name="model_beta",
        code="def add_numbers(a, b):\n    return a - b\n",
    )

    result = evaluate_submission(task, submission)

    assert result.passed is False
    assert result.score == 0.0
    assert result.error_type == "assertion_error"


def test_timeout_submission_fails_safely() -> None:
    task = BenchmarkTask(
        task_id="is_even",
        title="Check Even Number",
        prompt="Write is_even.",
        entrypoint="is_even",
        tests=[
            "assert is_even(2) is True",
        ],
        timeout_seconds=1,
    )

    submission = CodeSubmission(
        task_id="is_even",
        model_name="model_timeout",
        code="def is_even(number):\n    while True:\n        pass\n",
    )

    result = evaluate_submission(task, submission)

    assert result.passed is False
    assert result.score == 0.0
    assert result.error_type == "timeout"


def test_evaluate_all_returns_summary() -> None:
    tasks = [
        BenchmarkTask(
            task_id="sum_two_numbers",
            title="Sum Two Numbers",
            prompt="Write add_numbers.",
            entrypoint="add_numbers",
            tests=[
                "assert add_numbers(2, 3) == 5",
            ],
            timeout_seconds=2,
        )
    ]

    submissions = [
        CodeSubmission(
            task_id="sum_two_numbers",
            model_name="model_alpha",
            code="def add_numbers(a, b):\n    return a + b\n",
        ),
        CodeSubmission(
            task_id="sum_two_numbers",
            model_name="model_beta",
            code="def add_numbers(a, b):\n    return a - b\n",
        ),
    ]

    summary = evaluate_all(tasks, submissions)

    assert summary.total_submissions == 2
    assert summary.passed_submissions == 1
    assert summary.failed_submissions == 1
    assert summary.pass_rate == 50.0
    assert summary.average_score == 0.5