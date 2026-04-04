from typing import List
from pydantic import BaseModel

class RecommendationItem(BaseModel):
    courseId: str
    courseName: str
    category: str
    reason: str

class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
