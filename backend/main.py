
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.models import (
    LearnerProfile,
    ExternalDiagnosticResult,
    QuizSubmission,
)

from backend.services.level_estimator import estimate_initial_level
from backend.services.prediction_comparator import compare_prediction

from backend.services.vocabulary_quiz import (
    QUIZZES,
    get_quiz,
    calculate_score,
)

from backend.diagnostic_store import (
    save_diagnostic_result,
    get_latest_diagnostic_result,
)

from backend.estimate_store import (
    save_estimate,
    get_estimate,
)

from backend.database import initialize_database

from backend.experiment_store import (
    save_experiment_result,
    get_experiment_results,
)

from backend.learning_stage_store import (
    save_learning_stage,
    get_learning_stage,
)

from backend.services.learning_flow import get_next_step

from backend.services.experiment_analyzer import (
    analyze_experiment_results,
)

from backend.services.ai_feedback import (
    generate_experiment_feedback,
)
from backend.services.method_recommender import recommend_method
from backend.profile_store import save_profile, get_profile

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://alee-frontend.onrender.com",
        "https://alee-placement-test.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LearningStageRequest(BaseModel):
    learner_id: int
    stage: Literal[
        "placement_test",
        "placement_review",
        "content_learning",
        "vocabulary_quiz",
        "results_review",
    ]
    method: Literal["music", "story", "animation"] | None = None


class PracticeAnswer(BaseModel):
    question_id: int
    answer: str


@app.get("/")
def root():
    return {"message": "ALEE backend is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/learner/{learner_id}/learning-stage")
def read_learning_stage(learner_id: int):
    if learner_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="learner_id must be positive.",
        )

    stage_data = get_learning_stage(learner_id)

    if stage_data is None:
        return {
            "learner_id": learner_id,
            "message": "No learning stage has been saved for this learner.",
        }

    return stage_data


@app.post("/learner/learning-stage")
def update_learning_stage(data: LearningStageRequest):
    if data.learner_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="learner_id must be positive.",
        )

    try:
        saved_stage = save_learning_stage(
            learner_id=data.learner_id,
            current_stage=data.stage,
            current_method=data.method,
        )

        next_step = get_next_step(data.stage)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    if (
        next_step.get("url")
        and next_step["url"].startswith("REPLACE_")
    ):
        next_step["url"] = None
        next_step["message"] += (
            " The placement-test link has not been configured yet."
        )

    return {
        "message": "Learning stage saved successfully.",
        "stage_data": saved_stage,
        "next_step": next_step,
    }


@app.get("/learner/{learner_id}/next-step")
def read_next_step(learner_id: int):
    if learner_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="learner_id must be positive.",
        )

    stage_data = get_learning_stage(learner_id)

    if stage_data is None:
        return {
            "learner_id": learner_id,
            "message": "No learning stage has been saved for this learner.",
        }

    next_step = get_next_step(stage_data["current_stage"])

    if (
        next_step.get("url")
        and next_step["url"].startswith("REPLACE_")
    ):
        next_step["url"] = None
        next_step["message"] += (
            " The placement-test link has not been configured yet."
        )

    return {
        "learner_id": learner_id,
        "current_method": stage_data["current_method"],
        "next_step": next_step,
    }


@app.post("/practice/answer")
def practice_answer(data: PracticeAnswer):
    return {
        "message": "We received it successfully",
        "question_id": data.question_id,
        "answer": data.answer,
    }


@app.post("/learner/profile")
def create_learner_profile(profile: LearnerProfile):
    saved_profile = save_profile(profile)

    return {
        "message": "Learner profile saved successfully",
        "learner": saved_profile,
    }


@app.post("/learner/analyze")
def analyze_learner(profile: LearnerProfile):
    estimate = estimate_initial_level(profile)
    save_estimate(estimate)

    return {
        "learner": profile,
        "initial_estimate": estimate,
    }


@app.post("/diagnostic/result")
def receive_diagnostic_result(
    result: ExternalDiagnosticResult,
):
    saved_result = save_diagnostic_result(result)

    return {
        "message": "Diagnostic result saved successfully",
        "diagnostic_result": saved_result,
    }


@app.get("/diagnostic/latest")
def get_latest_diagnostic():
    result = get_latest_diagnostic_result()

    if result is None:
        return {"message": "No diagnostic result found"}

    return {"diagnostic_result": result}


@app.get("/learner/{learner_id}/prediction-comparison")
def get_prediction_comparison(learner_id: int):
    estimate = get_estimate(learner_id)

    if estimate is None:
        return {
            "message": "No initial estimate found for this learner",
            "learner_id": learner_id,
        }

    diagnostic = get_latest_diagnostic_result(learner_id)

    if diagnostic is None or diagnostic.learner_id != learner_id:
        return {
            "message": "No diagnostic result found for this learner",
            "learner_id": learner_id,
        }

    return compare_prediction(estimate, diagnostic)


@app.get("/experiments/quiz/{method}")
def get_experiment_quiz(method: str):
    if method not in QUIZZES:
        raise HTTPException(
            status_code=404,
            detail="Unknown learning method. Use music, story, or animation.",
        )

    quiz = get_quiz(method)

    # Never return correct_option to the frontend.
    return {
        "method": method,
        "vocabulary_set_id": quiz["vocabulary_set_id"],
        "questions": [
            {
                "id": question["id"],
                "word": question["word"],
                "question": question["question"],
                "options": question["options"],
            }
            for question in quiz["questions"]
        ],
    }


@app.post("/experiments/submit")
def submit_experiment(data: QuizSubmission):
    answers = [
        {
            "question_id": answer.question_id,
            "selected_option": answer.selected_option,
        }
        for answer in data.answers
    ]

    try:
        result = calculate_score(data.method, answers)
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    saved_result = save_experiment_result(
        learner_id=data.learner_id,
        method=result["method"],
        vocabulary_set_id=result["vocabulary_set_id"],
        score=result["score"],
        total_questions=result["total_questions"],
    )

    return {
        "message": "Experiment result saved successfully",
        "result": {
            **saved_result,
            "percentage": result["percentage"],
        },
    }


@app.get("/experiments/results/{learner_id}")
def get_learner_experiment_results(learner_id: int):
    if learner_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="learner_id must be positive.",
        )

    results = get_experiment_results(learner_id)

    return {
        "learner_id": learner_id,
        "results": [
            {
                **result,
                "percentage": round(
                    result["score"] / result["total_questions"] * 100,
                    2,
                ),
            }
            for result in results
        ],
    }


@app.get("/experiments/comparison/{learner_id}")
def compare_learning_methods(learner_id: int):
    if learner_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="learner_id must be positive.",
        )

    results = get_experiment_results(learner_id)
    methods = ("music", "story", "animation")
    comparison = {}

    for method in methods:
        method_results = [
            result
            for result in results
            if result["method"] == method
        ]

        if not method_results:
            comparison[method] = {
                "status": "not_completed",
                "attempts": 0,
                "latest_result": None,
            }
            continue

        latest = method_results[-1]
        total_questions = latest["total_questions"]

        comparison[method] = {
            "status": "completed",
            "attempts": len(method_results),
            "latest_result": {
                "score": latest["score"],
                "total_questions": total_questions,
                "percentage": (
                    round(
                        latest["score"] / total_questions * 100,
                        2,
                    )
                    if total_questions > 0
                    else None
                ),
                "created_at": latest["created_at"],
            },
        }

    completed_methods = [
        method
        for method in methods
        if comparison[method]["status"] == "completed"
    ]

    return {
        "learner_id": learner_id,
        "completed_methods": completed_methods,
        "all_methods_completed": len(completed_methods) == 3,
        "comparison": comparison,
        "interpretation": (
            "Scores describe quiz performance only. "
            "They do not establish which learning method is best."
        ),
    }


@app.get("/learner/{learner_id}/recommended-next-step")
def recommend_next_step(learner_id: int):
    if learner_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="learner_id must be positive.",
        )

    results = get_experiment_results(learner_id)
    methods = ("music", "story", "animation")

    completed_methods = {
        result["method"]
        for result in results
        if result["method"] in methods
    }

    remaining_methods = [
        method
        for method in methods
        if method not in completed_methods
    ]

    if not results:
        stage = "content_learning"
        method = "music"
        reason = (
            "No vocabulary quiz results have been recorded yet. "
            "Music is suggested as the first activity."
        )
    elif remaining_methods:
        stage = "content_learning"
        method = remaining_methods[0]
        reason = (
            "This method has no recorded vocabulary quiz result yet."
        )
    else:
        stage = "results_review"
        method = None
        reason = (
            "All three methods have recorded vocabulary quiz results. "
            "Review the results before drawing conclusions."
        )

    next_step = get_next_step(stage)

    return {
        "learner_id": learner_id,
        "recommended_stage": stage,
        "recommended_method": method,
        "reason": reason,
        "next_step": next_step,
        "completed_methods": [
            item for item in methods if item in completed_methods
        ],
        "remaining_methods": remaining_methods,
    }


@app.get("/experiments/analysis/{learner_id}")
def analyze_learner_experiments(learner_id: int):
    if learner_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="learner_id must be positive.",
        )

    results = get_experiment_results(learner_id)
    analysis = analyze_experiment_results(results)

    return {
        "learner_id": learner_id,
        "analysis": analysis,
    }


@app.get("/experiments/feedback/{learner_id}")
def get_experiment_feedback(learner_id: int):
    if learner_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="learner_id must be positive.",
        )

    results = get_experiment_results(learner_id)
    analysis = analyze_experiment_results(results)
    feedback = generate_experiment_feedback(analysis)

    return {
        "learner_id": learner_id,
        "analysis": analysis,
        "personalized_feedback": feedback,
    }

@app.post("/learner/recommend-method")
def recommend_learning_method(profile: LearnerProfile):
    return recommend_method(profile.model_dump())


@app.get("/learner/{learner_id}/recommend-method")
def recommend_saved_learning_method(learner_id: int):
    if learner_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="learner_id must be positive.",
        )

    profile = get_profile(learner_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Learner profile not found.",
        )

    return recommend_method(profile.model_dump())


@app.get("/learner/{learner_id}/profile")
def read_learner_profile(learner_id: int):
    if learner_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="learner_id must be positive.",
        )

    profile = get_profile(learner_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Learner profile not found.",
        )

    return {"learner": profile}