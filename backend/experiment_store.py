
from backend.database import get_connection


def save_experiment_result(
    learner_id: int,
    method: str,
    vocabulary_set_id: str,
    score: int,
    total_questions: int,
) -> dict:
    if learner_id <= 0:
        raise ValueError("learner_id must be positive.")

    if method not in {"music", "story", "animation"}:
        raise ValueError("Invalid learning method.")

    if not 0 <= score <= total_questions:
        raise ValueError("Score is outside the valid range.")

    if total_questions != 6:
        raise ValueError("Each experiment quiz must have six questions.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO learning_experiments (
                learner_id,
                method,
                vocabulary_set_id,
                score,
                total_questions
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                learner_id,
                method,
                vocabulary_set_id,
                score,
                total_questions,
            ),
        )

        row = connection.execute(
            """
            SELECT
                id,
                learner_id,
                method,
                vocabulary_set_id,
                score,
                total_questions,
                created_at
            FROM learning_experiments
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return dict(row)


def get_experiment_results(learner_id: int) -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                learner_id,
                method,
                vocabulary_set_id,
                score,
                total_questions,
                created_at
            FROM learning_experiments
            WHERE learner_id = ?
            ORDER BY id
            """,
            (learner_id,),
        ).fetchall()

    return [dict(row) for row in rows]
