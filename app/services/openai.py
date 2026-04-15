import json
from typing import Any, Dict, List
from fastapi import HTTPException
from app.core.clients import openai_client
from app.core.system_instructions import (
    SYSTEM_INSTRUCTIONS_FOR_QUIZ,
    SYSTEM_INSTRUCTIONS_FOR_RECOMMENDATION,
)
from app.schemas.quiz import Quiz
from app.schemas.recommendation import RecommendationResponse


def get_course_recommendations(
    all_courses: List[Dict[str, Any]],
    purchased_courses: List[Dict[str, Any]],
) -> Dict[str, Any]:
    prompt_payload = {
        "allCourses": all_courses,
        "purchasedCourses": purchased_courses,
    }
    try:
        response = openai_client.responses.parse(
            model="gpt-5.4-mini",
            text_format=RecommendationResponse,
            instructions=SYSTEM_INSTRUCTIONS_FOR_RECOMMENDATION,
            input=json.dumps(prompt_payload),
        )
    except Exception as e:
        error_msg = str(e).lower()
        if "insufficient_quota" in error_msg:
            raise HTTPException(500, "OpenAI credits exhausted")
        if "rate_limit" in error_msg:
            raise HTTPException(429, "Too many requests")
        raise HTTPException(500, "AI error")
    if not response.output_text:
        raise HTTPException(status_code=500,detail="OpenAI returned an empty response")

    return response.output_parsed


def get_course_based_quiz(courseName: str, courseDescription: str):
    prompt_payload = {"courseName": courseName, "courseDescription": courseDescription}
    try:
        response = openai_client.responses.parse(
            model="gpt-5.4-nano",
            instructions=SYSTEM_INSTRUCTIONS_FOR_QUIZ,
            text_format=Quiz,
            input=json.dumps(prompt_payload),
        )
    except Exception as e:
        error_msg = str(e).lower()
        if "insufficient_quota" in error_msg:
            raise HTTPException(500, "OpenAI credits exhausted")
        if "rate_limit" in error_msg:
            raise HTTPException(429, "Too many requests")
        raise HTTPException(500, "AI error")

    if not response.output_text:
        raise HTTPException(status_code=500, detail="openAI returned an empty response")
    return response.output_parsed
