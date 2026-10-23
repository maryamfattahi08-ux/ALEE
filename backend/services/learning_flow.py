
from typing import Literal


# Replace this placeholder with your real public placement-test URL.
PLACEMENT_TEST_URL = "REPLACE_WITH_PLACEMENT_TEST_URL"

# Public website containing the animation, music, and story activities.
CONTENT_WEBSITE_URL = "https://sea-turtle-wwl4g4.my.canva.site/"


LearningStage = Literal[
    "placement_test",
    "placement_review",
    "content_learning",
    "vocabulary_quiz",
    "results_review",
]


def get_next_step(stage: LearningStage) -> dict:
    """
    Return the message, URL, and action for a learning stage.

    This function provides stage instructions only.
    It does not automatically track learner progress or verify
    whether an activity or test has actually been completed.
    """

    if stage == "placement_test":
        return {
            "stage": "placement_test",
            "message": (
                "Before I assess your English level, please complete "
                "the placement test carefully. Answer every question "
                "to the best of your ability. Once you finish, return "
                "here so I can review your results."
            ),
            "url": PLACEMENT_TEST_URL,
            "action": "complete_placement_test",
        }

    if stage == "placement_review":
        return {
            "stage": "placement_review",
            "message": (
                "I've received your placement test results. "
                "Let's compare them with my initial estimate of your "
                "English level. I'll explain what the results suggest "
                "and point out any limitations in the assessment."
            ),
            "url": None,
            "action": "review_placement_result",
        }

    if stage == "content_learning":
        return {
            "stage": "content_learning",
            "message": (
                "Please visit the learning website below and complete "
                "the activity assigned to you. Depending on the "
                "learning method, watch the animation, listen to the "
                "song, or read the story or listen to its audio. "
                "Take your time to understand the content and pay "
                "attention to the vocabulary. When you finish, return "
                "here and tell me that you have completed the activity. "
                "I'll then provide the vocabulary quiz for that method."
            ),
            "url": CONTENT_WEBSITE_URL,
            "action": "complete_learning_content",
        }

    if stage == "vocabulary_quiz":
        return {
            "stage": "vocabulary_quiz",
            "message": (
                "Now it's time for your six-question vocabulary quiz. "
                "Choose the best answer for each question. Please answer "
                "without looking up the definitions so that your result "
                "better reflects what you remember from the activity."
            ),
            "url": None,
            "action": "start_vocabulary_quiz",
        }

    if stage == "results_review":
        return {
            "stage": "results_review",
            "message": (
                "You've completed the learning activities. Let's "
                "compare your results across animation, music, and "
                "story-based learning. I'll use your scores to offer "
                "a tentative recommendation about which method may "
                "be worth exploring further. Because each quiz is "
                "short, the results are an initial indication rather "
                "than definitive proof of which method works best for you."
            ),
            "url": None,
            "action": "review_experiment_results",
        }

    raise ValueError(f"Unsupported learning stage: {stage}")
