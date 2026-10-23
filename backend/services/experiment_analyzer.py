
from statistics import mean


VALID_METHODS = ("music", "story", "animation")


def analyze_experiment_results(results: list[dict]) -> dict:
    """
    Summarize recorded vocabulary quiz results without claiming
    that a higher score proves a learning method is better.
    """

    method_results = {
        method: [
            result
            for result in results
            if result.get("method") == method
        ]
        for method in VALID_METHODS
    }

    summary = {}

    for method, attempts in method_results.items():
        if not attempts:
            summary[method] = {
                "status": "not_completed",
                "attempts": 0,
                "latest_score": None,
                "latest_percentage": None,
                "average_percentage": None,
            }
            continue

        percentages = [
            round(
                result["score"] / result["total_questions"] * 100,
                2,
            )
            for result in attempts
            if result["total_questions"] > 0
        ]

        latest = attempts[-1]
        latest_percentage = round(
            latest["score"] / latest["total_questions"] * 100,
            2,
        )

        summary[method] = {
            "status": "completed",
            "attempts": len(attempts),
            "latest_score": latest["score"],
            "total_questions": latest["total_questions"],
            "latest_percentage": latest_percentage,
            "average_percentage": (
                round(mean(percentages), 2)
                if percentages
                else None
            ),
        }

    completed = [
        method
        for method in VALID_METHODS
        if summary[method]["status"] == "completed"
    ]

    if len(completed) < 2:
        interpretation = (
            "There is not enough completed-method data to compare "
            "at least two learning methods."
        )
        suggested_action = "complete_more_methods"
    else:
        latest_scores = {
            method: summary[method]["latest_percentage"]
            for method in completed
        }

        highest = max(latest_scores.values())
        lowest = min(latest_scores.values())

        if highest == lowest:
            interpretation = (
                "The latest quiz percentages are equal across all "
                "completed methods. These results do not distinguish "
                "one method as better."
            )
            suggested_action = "collect_more_evidence"
        else:
            interpretation = (
                "The latest quiz percentages differ across methods. "
                "This is a descriptive difference in quiz performance, "
                "not proof that one method causes better learning."
            )
            suggested_action = "review_differences"

    return {
        "methods": summary,
        "completed_methods": completed,
        "all_methods_completed": len(completed) == len(VALID_METHODS),
        "interpretation": interpretation,
        "suggested_action": suggested_action,
        "limitations": [
            "Short vocabulary quizzes provide limited evidence.",
            "Repeated attempts may affect scores through practice.",
            "Quiz scores alone do not establish long-term retention.",
            "A higher score does not prove that a method caused better learning.",
        ],
    }
