from fastapi import APIRouter, Body, Depends, HTTPException

from app.core.security import check_secret_key
from app.schemas.course import RecommendationRequest

from app.services.gemini_service import (
    get_course_based_quiz,
    get_course_recommendations,
)

router = APIRouter()


@router.post("/getCourseRecommendations")
async def recommend_courses(
    body: RecommendationRequest, _: None = Depends(check_secret_key)
):
    purchased_courses = [course.model_dump() for course in body.enrolled_courses]
    all_courses = [course.model_dump() for course in body.all_courses]

    try:
        recommendations = get_course_recommendations(
            all_courses=all_courses,
            purchased_courses=purchased_courses,
        )
        return recommendations
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(exc)}",
        ) from exc


@router.post("/getCourseQuiz")
def get_course_quiz(
    courseName: str = Body(),
    courseDescription: str = Body(),
    _: None = Depends(check_secret_key),
):
    try:
        response = get_course_based_quiz(courseName, courseDescription)
        return response
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to get Quiz Questions.")
