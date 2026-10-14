
from backend.database import get_connection
from backend.models import InitialLevelEstimate


def save_estimate(
    estimate: InitialLevelEstimate
) -> InitialLevelEstimate:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO initial_estimates (
                learner_id,
                estimated_level,
                confidence,
                evidence
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(learner_id) DO UPDATE SET
                estimated_level = excluded.estimated_level,
                confidence = excluded.confidence,
                evidence = excluded.evidence
            """,
            (
                estimate.learner_id,
                estimate.estimated_level,
                estimate.confidence,
                estimate.evidence,
            ),
        )

    return estimate


def get_estimate(
    learner_id: int
) -> InitialLevelEstimate | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT learner_id, estimated_level, confidence, evidence
            FROM initial_estimates
            WHERE learner_id = ?
            """,
            (learner_id,),
        ).fetchone()

    if row is None:
        return None

    return InitialLevelEstimate(**dict(row))
