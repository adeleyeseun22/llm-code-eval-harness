from pydantic import BaseModel, Field


class BenchmarkTask(BaseModel):
    task_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    entrypoint: str = Field(min_length=1)
    tests: list[str] = Field(min_length=1)
    timeout_seconds: int = Field(default=2, ge=1, le=30)


class CodeSubmission(BaseModel):
    task_id: str = Field(min_length=1)
    model_name: str = Field(min_length=1)
    code: str = Field(min_length=1)


class EvaluationResult(BaseModel):
    task_id: str
    title: str
    model_name: str
    passed: bool
    score: float
    runtime_ms: float
    error_type: str | None = None
    error_message: str | None = None
    stdout: str = ""
    stderr: str = ""


class EvaluationSummary(BaseModel):
    total_submissions: int
    passed_submissions: int
    failed_submissions: int
    pass_rate: float
    average_score: float
    results: list[EvaluationResult]