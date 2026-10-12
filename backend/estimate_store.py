from backend.models import InitialLevelEstimate


estimate_records: dict[int, InitialLevelEstimate] = {}


def save_estimate(
    estimate: InitialLevelEstimate
) -> InitialLevelEstimate:
    estimate_records[estimate.learner_id] = estimate
    return estimate


def get_estimate(
    learner_id: int
) -> InitialLevelEstimate | None:
    return estimate_records.get(learner_id)