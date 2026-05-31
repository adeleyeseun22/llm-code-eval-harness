from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from llm_code_eval_harness.evaluator import evaluate_all
from llm_code_eval_harness.loader import load_benchmark_tasks, load_code_submissions
from llm_code_eval_harness.report import (
    format_console_summary,
    save_csv_report,
    save_json_report,
)

app = typer.Typer(
    help="Evaluate AI-generated code submissions against benchmark tests.",
    no_args_is_help=True,
)

console = Console()


@app.callback()
def cli() -> None:
    """
    LLM code evaluation command-line interface.
    """


@app.command()
def evaluate(
    benchmark_file: Annotated[
        Path,
        typer.Argument(help="Path to the benchmark tasks JSON file."),
    ],
    submissions_file: Annotated[
        Path,
        typer.Argument(help="Path to the code submissions JSON file."),
    ],
    json_report: Annotated[
        Path,
        typer.Option(
            "--json-report",
            "-j",
            help="Path where the JSON evaluation report should be saved.",
        ),
    ] = Path("reports/evaluation_report.json"),
    csv_report: Annotated[
        Path,
        typer.Option(
            "--csv-report",
            "-c",
            help="Path where the CSV evaluation report should be saved.",
        ),
    ] = Path("reports/evaluation_report.csv"),
) -> None:
    """
    Evaluate code submissions against benchmark tasks.
    """
    try:
        tasks = load_benchmark_tasks(benchmark_file)
        submissions = load_code_submissions(submissions_file)
        summary = evaluate_all(tasks, submissions)

        console.print(
            Panel(
                format_console_summary(summary),
                title="LLM Code Evaluation Harness",
                expand=False,
            )
        )

        save_json_report(summary, json_report)
        save_csv_report(summary.results, csv_report)

        console.print(f"\nJSON report saved to: [bold green]{json_report}[/bold green]")
        console.print(f"CSV report saved to: [bold green]{csv_report}[/bold green]")

    except Exception as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1) from error


def main() -> None:
    app()


if __name__ == "__main__":
    main()