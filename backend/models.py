from pydantic import BaseModel


class LearnerProfile(BaseModel):
    id: int
    name: str
    age: int
    goal: str

    years_learning: int
    days_per_week: int
    minutes_per_session: int

    learning_consistency: str
    learning_mode: str
    formal_learning: bool
    self_study: bool

    skills_practiced: str
    previous_level: str
    recent_breaks: str

class Skill(BaseModel):
    id: int
    name: str
    description: str


class DiagnosticResult(BaseModel):
    learner_id: int
    skill_id: int
    score: int
    level: str


class LearningMethod(BaseModel):
    id: int
    name: str
    description: str


class ExperimentResult(BaseModel):
    learner_id: int
    method_id: int
    skill_id: int
    score: int
    effectiveness: str


class InitialLevelEstimate(BaseModel):
    learner_id: int
    estimated_level: str
    confidence: int
    evidence: str

class SkillResult(BaseModel):
    skill: str
    level: str
    score: int
    total: int
    correct: int
    incorrect: int


class QuestionResult(BaseModel):
    question_id: int
    skill: str
    level: str
    correct: bool


class ExternalDiagnosticResult(BaseModel):
    learner_id: int
    diagnostic_name: str
    overall_level: str
    overall_score: int
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    skill_results: list[SkillResult]
    question_results: list[QuestionResult]