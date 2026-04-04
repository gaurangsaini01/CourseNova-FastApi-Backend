from typing import List
from pydantic import BaseModel

class Question(BaseModel):
    question: str
    options: List[str]
    answer: str

class Quiz(BaseModel):
    questions: List[Question]
