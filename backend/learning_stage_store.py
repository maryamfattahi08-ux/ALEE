
from backend.database import get_connection


VALID_STAGES = {
    "placement_test",
    "placement_review",
    "content_learning",
    "vocabulary_quiz",
    "results_review",
}

VALID_METHODS = {"music", "story", "animation"}


def save_learning_stage(
    learner_id: int,
    current_stage: str,
    current_method: str | None = None,
) -> dict:
    if learner_id <= 0:
        raise ValueError("learner_id must be positive.")

    if current_stage not in VALID_STAGES:
        raise ValueError("Invalid learning stage.")

    if current_method is not None and current_method not in VALID_METHODS:
        raise ValueError("Invalid learning method.")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO learner_learning_stages (
                learner_id, current_stage, current_method, updated_at
            )
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(learner_id) DO UPDATE SET
                current_stage = excluded.current_stage,
                current_method = excluded.current_method,
                updated_at = CURRENT_TIMESTAMP
            """,
            (learner_id, current_stage, current_method),
        )

        row = connection.execute(
            """
            SELECT learner_id, current_stage, current_method, updated_at
            FROM learner_learning_stages
            WHERE learner_id = ?
            """,
            (learner_id,),
        ).fetchone()

    return dict(row)


def get_learning_stage(learner_id: int) -> dict | None:
    if learner_id <= 0:
        raise ValueError("learner_id must be positive.")

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT learner_id, current_stage, current_method, updated_at
            FROM learner_learning_stages
            WHERE learner_id = ?
            """,
            (learner_id,),
        ).fetchone()

    return dict(row) if row else None
