from backend.models import LearnerProfile, InitialLevelEstimate


def estimate_initial_level(
    profile: LearnerProfile
) -> InitialLevelEstimate:

    # 1. Calculate weekly learning exposure
    weekly_minutes = (
        profile.days_per_week
        * profile.minutes_per_session
    )

    # 2. Estimate yearly learning exposure
    annual_minutes = weekly_minutes * 52

    # 3. Estimate total learning exposure
    total_exposure = (
        annual_minutes
        * profile.years_learning
    )

    # 4. Create an initial hypothesis
    estimated_level = "A1/A2"
    confidence = 30

    # 5. Use exposure, consistency, and learning mode
    if (
        total_exposure >= 150000
        and profile.learning_consistency == "high"
        and profile.learning_mode == "active"
    ):
        estimated_level = "B1/B2"
        confidence = 55

    elif (
        total_exposure >= 70000
        and profile.learning_consistency in ["high", "medium"]
    ):
        estimated_level = "A2/B1"
        confidence = 45

    # 6. Keep the learner's previous level
    # as separate evidence
    previous_level = profile.previous_level.upper()

    # 7. Compare previous level with the initial hypothesis
    if previous_level:
        if previous_level in estimated_level:
            evidence_alignment = "compatible"

        else:
            evidence_alignment = "mismatch"

    else:
        evidence_alignment = "no_previous_level"

    # 8. Explain the evidence
    evidence = (
        f"Estimated total exposure: {total_exposure} minutes. "
        f"Learning consistency: {profile.learning_consistency}. "
        f"Learning mode: {profile.learning_mode}. "
        f"Previous reported level: {profile.previous_level}. "
        f"Previous level alignment: {evidence_alignment}. "
        f"This is an initial hypothesis, not a diagnostic result."
    )

    # 9. Return the initial hypothesis
    return InitialLevelEstimate(
        learner_id=profile.id,
        estimated_level=estimated_level,
        confidence=confidence,
        evidence=evidence
    )
