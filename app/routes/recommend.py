from fastapi import APIRouter, Body, Depends, HTTPException
from app.services.chatbot import ask_query_from_chatbot
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

    return get_course_recommendations(
        all_courses=all_courses,
        purchased_courses=purchased_courses,
    )


@router.post("/getCourseQuiz")
def get_course_quiz(
    courseName: str = Body(),
    courseDescription: str = Body(),
    _: None = Depends(check_secret_key),
):
    return get_course_based_quiz(courseName, courseDescription)


@router.post("/chatbot")
def chatbot(
    query: str = Body(),
    course_id: str = Body(),
    _: None = Depends(check_secret_key),
):
    return ask_query_from_chatbot(query, course_id)
