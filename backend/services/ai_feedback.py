
def generate_experiment_feedback(analysis: dict) -> dict:
    """
    Generate a user-friendly explanation from experiment analysis.
    This is rule-based feedback, not an actual AI model.
    """

    methods = analysis.get("methods", {})
    completed = analysis.get("completed_methods", [])

    if len(completed) < 2:
        message = (
            "There is not enough quiz data to compare your learning "
            "methods yet. Complete at least two methods to receive "
            "a more useful comparison."
        )
        recommendation = (
            "Complete another learning activity and its vocabulary quiz."
        )

    else:
        percentages = {
            method: methods[method]["latest_percentage"]
            for method in completed
            if methods.get(method, {}).get("latest_percentage") is not None
        }

        if len(percentages) < 2:
            message = (
                "There is not enough valid quiz data to compare "
                "your completed learning methods."
            )
            recommendation = (
                "Complete the missing quizzes before comparing methods."
            )

        else:
            highest = max(percentages.values())
            lowest = min(percentages.values())

            if highest == lowest:
                message = (
                    "You achieved the same percentage on the latest "
                    "vocabulary quiz for every completed learning method. "
                    "Your current results do not identify one method "
                    "as more promising than the others."
                )
                recommendation = (
                    "Try a delayed vocabulary quiz later to check "
                    "how well you retain the words over time."
                )

            else:
                best_methods = [
                    method
                    for method, percentage in percentages.items()
                    if percentage == highest
                ]

                if len(best_methods) == 1:
                    best_method = best_methods[0]
                    message = (
                        f"You achieved your highest latest quiz score "
                        f"after the {best_method}-based activity "
                        f"({highest}%). This suggests that this method "
                        f"may be promising for you, but the result alone "
                        f"does not prove it is the most effective method."
                    )
                    recommendation = (
                        "Repeat the comparison under similar conditions "
                        "and take a delayed vocabulary quiz before "
                        "deciding whether this method suits you better."
                    )
                else:
                    names = ", ".join(best_methods)
                    message = (
                        f"The highest latest quiz percentage was shared "
                        f"by these methods: {names} ({highest}%). "
                        f"The current results do not identify a single "
                        f"leading method."
                    )
                    recommendation = (
                        "Collect more evidence, including delayed "
                        "vocabulary-retention results, before choosing "
                        "between these methods."
                    )

    return {
        "feedback": message,
        "recommendation": recommendation,
        "based_on": "latest_vocabulary_quiz_percentages",
        "is_actual_ai_generated": False,
    }
