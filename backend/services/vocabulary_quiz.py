
from typing import Literal


Method = Literal["music", "story", "animation"]


QUIZZES = {
    "music": {
        "vocabulary_set_id": "music_v1",
        "questions": [
            {
                "id": 1,
                "word": "Ambivalent",
                "question": "A person feels both excited about leaving and sad about saying goodbye. Which word best describes these mixed feelings?",
                "options": {
                    "A": "Ambivalent",
                    "B": "Certain",
                    "C": "Indifferent",
                    "D": "Relieved",
                },
                "correct_option": "A",
            },
            {
                "id": 2,
                "word": "Ambivalent",
                "question": "Which sentence uses 'ambivalent' correctly?",
                "options": {
                    "A": "She was ambivalent, feeling both hopeful and anxious about the decision.",
                    "B": "She was ambivalent because she had made up her mind completely.",
                    "C": "The ambivalent table was made of wood.",
                    "D": "He ambivalent the letter yesterday.",
                },
                "correct_option": "A",
            },
            {
                "id": 3,
                "word": "Ostensibly",
                "question": "The meeting was ostensibly about planning, but everyone knew the real purpose was to settle an argument. What does 'ostensibly' mean here?",
                "options": {
                    "A": "Secretly and illegally",
                    "B": "Apparently or supposedly",
                    "C": "Without any reason",
                    "D": "Immediately and completely",
                },
                "correct_option": "B",
            },
            {
                "id": 4,
                "word": "Ostensibly",
                "question": "Which sentence best illustrates 'ostensibly'?",
                "options": {
                    "A": "Ostensibly, he visited to return a book, though he really wanted to talk.",
                    "B": "She ostensibly the window every morning.",
                    "C": "The ostensibly was blue and round.",
                    "D": "He ran ostensibly quickly to win the race.",
                },
                "correct_option": "A",
            },
            {
                "id": 5,
                "word": "Corroborate",
                "question": "Several independent records support a witness's account. The records help to…",
                "options": {
                    "A": "Contradict the account",
                    "B": "Corroborate the account",
                    "C": "Conceal the account",
                    "D": "Forget the account",
                },
                "correct_option": "B",
            },
            {
                "id": 6,
                "word": "Corroborate",
                "question": "Which piece of evidence would best corroborate someone's claim that it rained last night?",
                "options": {
                    "A": "A friend saying they dislike rain",
                    "B": "A prediction made next week",
                    "C": "A weather station's recorded rainfall from last night",
                    "D": "A picture of a sunny day last month",
                },
                "correct_option": "C",
            },
        ],
    },

    "story": {
        "vocabulary_set_id": "story_v1",
        "questions": [
            {
                "id": 1,
                "word": "Nuanced",
                "question": "A nuanced explanation recognizes that a problem has several subtle aspects rather than one simple cause. What does 'nuanced' mean?",
                "options": {
                    "A": "Oversimplified",
                    "B": "Showing subtle distinctions",
                    "C": "Completely unrelated",
                    "D": "Impossible to explain",
                },
                "correct_option": "B",
            },
            {
                "id": 2,
                "word": "Incongruous",
                "question": "A person wears a formal tuxedo to a muddy camping trip. The outfit seems…",
                "options": {
                    "A": "Incongruous",
                    "B": "Practical",
                    "C": "Unavoidable",
                    "D": "Conventional",
                },
                "correct_option": "A",
            },
            {
                "id": 3,
                "word": "Incongruous",
                "question": "Which sentence uses 'incongruous' correctly?",
                "options": {
                    "A": "The incongruous quietly opened the door.",
                    "B": "Her cheerful laughter felt incongruous during the solemn ceremony.",
                    "C": "He incongruous the answer carefully.",
                    "D": "They bought an incongruous of bread.",
                },
                "correct_option": "B",
            },
            {
                "id": 4,
                "word": "Perpetuate",
                "question": "If a rumor keeps spreading because people repeat it, their actions may…",
                "options": {
                    "A": "Perpetuate the rumor",
                    "B": "Eliminate the rumor",
                    "C": "Verify every detail",
                    "D": "Interrupt the past",
                },
                "correct_option": "A",
            },
            {
                "id": 5,
                "word": "Mitigate",
                "question": "A new policy reduces the harmful effects of pollution. The policy helps to…",
                "options": {
                    "A": "Intensify the harm",
                    "B": "Ignore the harm",
                    "C": "Mitigate the harm",
                    "D": "Predict the harm",
                },
                "correct_option": "C",
            },
            {
                "id": 6,
                "word": "Mitigate",
                "question": "Which action would best mitigate the effects of a long power outage?",
                "options": {
                    "A": "Disconnecting all backup power sources",
                    "B": "Providing safe temporary charging and cooling stations",
                    "C": "Ignoring reports from affected residents",
                    "D": "Preventing repair crews from entering the area",
                },
                "correct_option": "B",
            },
        ],
    },

    "animation": {
        "vocabulary_set_id": "animation_v1",
        "questions": [
            {
                "id": 1,
                "word": "Ubiquitous",
                "question": "Smartphones are ubiquitous in many cities. What does 'ubiquitous' mean?",
                "options": {
                    "A": "Rare and expensive",
                    "B": "Found almost everywhere",
                    "C": "Newly invented",
                    "D": "Difficult to repair",
                },
                "correct_option": "B",
            },
            {
                "id": 2,
                "word": "Inadvertently",
                "question": "She inadvertently deleted the file while trying to rename it. What does 'inadvertently' mean?",
                "options": {
                    "A": "Deliberately",
                    "B": "With great care",
                    "C": "Unintentionally",
                    "D": "After asking permission",
                },
                "correct_option": "C",
            },
            {
                "id": 3,
                "word": "Inadvertently",
                "question": "Which situation best illustrates 'inadvertently'?",
                "options": {
                    "A": "He intentionally hid the key.",
                    "B": "She accidentally sent the message to the wrong person.",
                    "C": "They carefully followed the instructions.",
                    "D": "He refused to answer the question.",
                },
                "correct_option": "B",
            },
            {
                "id": 4,
                "word": "Substantiate",
                "question": "A scientist provides reliable data to support a claim. The data help to…",
                "options": {
                    "A": "Substantiate the claim",
                    "B": "Dismiss all evidence",
                    "C": "Change the subject",
                    "D": "Hide the findings",
                },
                "correct_option": "A",
            },
            {
                "id": 5,
                "word": "Intransigent",
                "question": "Someone refuses to reconsider their position despite reasonable arguments. This person is…",
                "options": {
                    "A": "Flexible",
                    "B": "Intransigent",
                    "C": "Uncertain",
                    "D": "Cooperative",
                },
                "correct_option": "B",
            },
            {
                "id": 6,
                "word": "Intransigent",
                "question": "Which response best demonstrates an intransigent attitude?",
                "options": {
                    "A": "I'll review the evidence and reconsider.",
                    "B": "Let's find a compromise.",
                    "C": "I will not change my position, no matter what evidence you provide.",
                    "D": "I need more information before deciding.",
                },
                "correct_option": "C",
            },
        ],
    },
}


def get_quiz(method: Method) -> dict:
    return QUIZZES[method]


def calculate_score(method: Method, answers: list[dict]) -> dict:
    quiz = get_quiz(method)
    questions_by_id = {
        question["id"]: question
        for question in quiz["questions"]
    }

    if len(answers) != 6:
        raise ValueError("Exactly six answers are required.")

    submitted_ids = [answer["question_id"] for answer in answers]

    if len(set(submitted_ids)) != 6:
        raise ValueError("Each question must be answered exactly once.")

    if set(submitted_ids) != set(questions_by_id):
        raise ValueError("Submitted question IDs do not match this quiz.")

    score = 0

    for answer in answers:
        question = questions_by_id[answer["question_id"]]
        selected_option = answer["selected_option"].upper()

        if selected_option not in question["options"]:
            raise ValueError("Invalid option.")

        if selected_option == question["correct_option"]:
            score += 1

    total = len(questions_by_id)

    return {
        "method": method,
        "vocabulary_set_id": quiz["vocabulary_set_id"],
        "score": score,
        "total_questions": total,
        "percentage": round((score / total) * 100, 2),
    }
