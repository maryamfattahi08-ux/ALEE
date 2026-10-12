from backend.models import (
    InitialLevelEstimate,
    ExternalDiagnosticResult,
)


CEFR_LEVELS = {
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1": 5,
    "C2": 6,
}


def compare_prediction(
    estimate: InitialLevelEstimate,
    diagnostic: ExternalDiagnosticResult,
) -> dict:

    predicted_level = estimate.estimated_level.strip().upper()
    observed_level = diagnostic.overall_level.strip().upper()

    if observed_level not in CEFR_LEVELS:
        raise ValueError(
            f"Unsupported observed CEFR level: {observed_level}"
        )

    # A prediction such as B1/B2 represents a range.
    predicted_levels = predicted_level.split("/")

    if not all(
        level in CEFR_LEVELS
        for level in predicted_levels
    ):
        raise ValueError(
            f"Unsupported predicted CEFR level: {predicted_level}"
        )

    predicted_min = min(
        CEFR_LEVELS[level]
        for level in predicted_levels
    )

    predicted_max = max(
        CEFR_LEVELS[level]
        for level in predicted_levels
    )

    observed_value = CEFR_LEVELS[observed_level]

    if predicted_min <= observed_value <= predicted_max:
        status = "within_prediction_range"
        difference = 0

    elif observed_value < predicted_min:
        status = "overestimated"
        difference = predicted_min - observed_value

    else:
        status = "underestimated"
        difference = observed_value - predicted_max

    return {
        "learner_id": estimate.learner_id,
        "predicted_level": predicted_level,
        "observed_level": observed_level,
        "prediction_status": status,
        "level_difference": difference,
        "diagnostic_score": diagnostic.overall_score,
    }