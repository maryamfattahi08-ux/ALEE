from fastapi import FastAPI
from pydantic import BaseModel
from backend.models import LearnerProfile
from backend.services.level_estimator import estimate_initial_level
from backend.models import ExternalDiagnosticResult
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

    return {
        "learner": profile,
        "initial_estimate": estimate
    }


@app.post('/diagnostic/result')
def receive_diagnostic_result(
    result: ExternalDiagnosticResult
):
    return {
        "message": "Diagnostic result received successfully",
        "diagnostic_result": result
    }