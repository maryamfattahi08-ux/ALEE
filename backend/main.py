from fastapi import FastAPI
app = FastAPI()

@app.get ('/')
def root():
    return {'message': 'ALEE backend is running'}


@app.get ('/health')
def health_check():
    return {'status':'healthy'}

from pydantic import BaseModel
class PracticeAnswer(BaseModel):
    question_id: int
    answer: str

@app.post('/practice/answer')
def practice_answer(data: PracticeAnswer):
    return {"message": "We received the answer successfully"}
