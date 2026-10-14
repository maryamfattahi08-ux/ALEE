from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.models import (
    LearnerProfile,
    ExternalDiagnosticResult,
)

from backend.services.level_estimator import estimate_initial_level
from backend.services.prediction_comparator import compare_prediction

from backend.diagnostic_store import (
    save_diagnostic_result,
    get_latest_diagnostic_result,
)

from backend.estimate_store import (
    save_estimate,
    get_estimate,
)
from contextlib import asynccontextmanager
from backend.database import initialize_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get ('/')
def root():
    return {'message': 'ALEE backend is running'}


@app.get ('/health')
def health_check():
    return {'status':'healthy'}

class PracticeAnswer(BaseModel):
    question_id: int
    answer: str

@app.post('/practice/answer')
def practice_answer(data: PracticeAnswer):
    return {'message':'we receved it successfully',
    'question_id':data.question_id,
    'answer':data.answer}

@app.post('/learner/profile')
def create_learner_profile(profile: LearnerProfile):
    return{
        'message':'learner profile received successfully',
        "learner": profile
    }

@app.post('/learner/analyze')
def analyze_learner(profile: LearnerProfile):
    estimate = estimate_initial_level(profile)

    save_estimate(estimate)

    return {
        "learner": profile,
        "initial_estimate": estimate
    }


@app.post('/diagnostic/result')
def receive_diagnostic_result(
    result: ExternalDiagnosticResult
):

    saved_result = save_diagnostic_result(result)

    return {
        "message": "Diagnostic result saved successfully",
        "diagnostic_result": saved_result
    }

@app.get('/diagnostic/latest')
def get_latest_diagnostic():

    result = get_latest_diagnostic_result()

    if result is None:
        return {
            "message": "No diagnostic result found"
        }

    return {
        "diagnostic_result": result
    }

@app.get("/learner/{learner_id}/prediction-comparison")
def get_prediction_comparison(learner_id: int):

    estimate = get_estimate(learner_id)

    if estimate is None:
        return {
            "message": "No initial estimate found for this learner",
            "learner_id": learner_id
        }

    diagnostic = get_latest_diagnostic_result(learner_id)

    if diagnostic is None:
        return {
            "message": "No diagnostic result found",
            "learner_id": learner_id
        }

    if diagnostic.learner_id != learner_id:
        return {
            "message": "No diagnostic result found for this learner",
            "learner_id": learner_id
        }

    return compare_prediction(estimate, diagnostic)