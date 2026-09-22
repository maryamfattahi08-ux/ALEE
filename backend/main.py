from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

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




