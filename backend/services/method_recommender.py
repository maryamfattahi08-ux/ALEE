
METHOD_DETAILS = {
    "music": {
        "name": "Music-based learning",
        "description": (
            "Learn vocabulary through songs, lyrics, "
            "rhythm, and repeated listening."
        ),
    },
    "story": {
        "name": "Story-based learning",
        "description": (
            "Learn vocabulary through narratives, "
            "characters, and meaningful contexts."
        ),
    },
    "animation": {
        "name": "Animation-based learning",
        "description": (
            "Learn vocabulary through animated scenes, "
            "visual context, and dialogue."
        ),
    },
}


def recommend_method(profile: dict) -> dict:
    """
    Recommend a learning method using explicit profile evidence.
    This initial version uses transparent rules, not an AI model.
    """

    learning_mode = profile.get("learning_mode", "").strip().lower()
    consistency = profile.get(
        "learning_consistency", ""
    ).strip().lower()

    goal = profile.get("goal", "").strip()
    previous_level = profile.get(
        "previous_level", ""
    ).strip()

    scores = {
        "music": 0,
        "story": 0,
        "animation": 0,
    }
    reasons = []

    # Use a preference only when the profile explicitly provides one.
    if learning_mode in {"music", "story", "animation"}:
        scores[learning_mode] += 3
        reasons.append(
            f"The recorded learning mode is {learning_mode}."
        )

    # These profile fields are contextual evidence, not proof
    # that a particular method is better.
    if consistency:
        reasons.append(
            f"Recorded learning consistency: {consistency}."
        )

    if goal:
        reasons.append(f"Learning goal: {goal}.")

    if previous_level:
        reasons.append(
            f"Previously reported level: {previous_level}."
        )

    highest_score = max(scores.values())
    leading_methods = [
        method
        for method, score in scores.items()
        if score == highest_score
    ]

    if highest_score == 0:
        return {
            "status": "insufficient_preference_data",
            "recommended_method": None,
            "method_name": None,
            "description": (
                "There is not enough explicit preference "
                "information to select one learning method."
            ),
            "reasons": reasons,
            "next_action": (
                "Ask the learner which format they prefer: "
                "music, stories, or animation."
            ),
        }

    if len(leading_methods) > 1:
        return {
            "status": "no_unique_recommendation",
            "recommended_method": None,
            "method_name": None,
            "description": (
                "The available profile information does not "
                "distinguish one method from the others."
            ),
            "reasons": reasons,
            "next_action": (
                "Ask the learner about their preferred "
                "learning format."
            ),
        }

    method = leading_methods[0]
    details = METHOD_DETAILS[method]

    return {
        "status": "recommended",
        "recommended_method": method,
        "method_name": details["name"],
        "description": details["description"],
        "reasons": reasons,
        "next_action": (
            "Present the recommended learning activity "
            "and let the learner try it."
        ),
        "is_actual_ai_generated": False,
    }
