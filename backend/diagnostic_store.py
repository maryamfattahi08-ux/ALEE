
import json

from backend.database import get_connection
from backend.models import ExternalDiagnosticResult


def save_diagnostic_result(
    result: ExternalDiagnosticResult,
) -> ExternalDiagnosticResult:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO diagnostic_results (
                learner_id,
                diagnostic_name,
                overall_level,
                overall_score,
                total_questions,
                correct_answers,
                incorrect_answers,
                result_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result.learner_id,
                result.diagnostic_name,
                result.overall_level,
                result.overall_score,
                result.total_questions,
                result.correct_answers,
                result.incorrect_answers,
                result.model_dump_json(),
            ),
        )

    return result


def get_latest_diagnostic_result(
    learner_id: int | None = None,
) -> ExternalDiagnosticResult | None:
    with get_connection() as connection:
        if learner_id is None:
            row = connection.execute(
                """
                SELECT result_json
                FROM diagnostic_results
                ORDER BY id DESC
                LIMIT 1
                """
            ).fetchone()
        else:
            row = connection.execute(
                """
                SELECT result_json
                FROM diagnostic_results
                WHERE learner_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (learner_id,),
            ).fetchone()

    if row is None:
        return None

    return ExternalDiagnosticResult.model_validate_json(
        row["result_json"]
    )


def get_diagnostic_history(
    learner_id: int,
) -> list[ExternalDiagnosticResult]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT result_json
            FROM diagnostic_results
            WHERE learner_id = ?
            ORDER BY id ASC
            """,
            (learner_id,),
        ).fetchall()

    return [
        ExternalDiagnosticResult.model_validate_json(
            row["result_json"]
        )
        for row in rows
    ]
