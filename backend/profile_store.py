
from backend.database import get_connection
from backend.models import LearnerProfile


def save_profile(profile: LearnerProfile) -> LearnerProfile:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO learner_profiles (
                id,
                name,
                age,
                goal,
                years_learning,
                days_per_week,
                minutes_per_session,
                learning_consistency,
                learning_mode,
                formal_learning,
                self_study,
                skills_practiced,
                previous_level,
                recent_breaks
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                age = excluded.age,
                goal = excluded.goal,
                years_learning = excluded.years_learning,
                days_per_week = excluded.days_per_week,
                minutes_per_session = excluded.minutes_per_session,
                learning_consistency = excluded.learning_consistency,
                learning_mode = excluded.learning_mode,
                formal_learning = excluded.formal_learning,
                self_study = excluded.self_study,
                skills_practiced = excluded.skills_practiced,
                previous_level = excluded.previous_level,
                recent_breaks = excluded.recent_breaks
            """,
            (
                profile.id,
                profile.name,
                profile.age,
                profile.goal,
                profile.years_learning,
                profile.days_per_week,
                profile.minutes_per_session,
                profile.learning_consistency,
                profile.learning_mode,
                profile.formal_learning,
                profile.self_study,
                profile.skills_practiced,
                profile.previous_level,
                profile.recent_breaks,
            ),
        )

    return profile


def get_profile(learner_id: int) -> LearnerProfile | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM learner_profiles
            WHERE id = ?
            """,
            (learner_id,),
        ).fetchone()

    if row is None:
        return None

    return LearnerProfile(**dict(row))
