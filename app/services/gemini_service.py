import json
from typing import Any, Dict, List
from fastapi import HTTPException
from google.genai import types
from app.core.clients import gemini_client
from app.core.system_instructions import (
    SYSTEM_INSTRUCTIONS_FOR_QUIZ,
    SYSTEM_INSTRUCTIONS_FOR_RECOMMENDATION,
)
from app.schemas.quiz import Quiz
from app.schemas.recommendation import RecommendationResponse


def _parse_json_response(raw_text: str) -> Dict[str, Any]:
    cleaned_text = raw_text.strip()

    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.strip("`")
        if cleaned_text.startswith("json"):
            cleaned_text = cleaned_text[4:].strip()

    parsed = json.loads(cleaned_text)

    if not isinstance(parsed, dict):
        raise ValueError("Gemini response is not a JSON object")

    return parsed


def get_course_recommendations(
    all_courses: List[Dict[str, Any]],
    purchased_courses: List[Dict[str, Any]],
) -> Dict[str, Any]:
    prompt_payload = {
        "allCourses": all_courses,
        "purchasedCourses": purchased_courses,
    }
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS_FOR_RECOMMENDATION,
            response_mime_type="application/json",
            response_schema=RecommendationResponse,
        ),
        contents=json.dumps(prompt_payload),
    )

    if response.parsed:
        return response.parsed.model_dump()

    if not response.text:
        raise HTTPException(status_code=500,detail="Gemini returned an empty response")

    return _parse_json_response(response.text)


def get_course_based_quiz(courseName: str, courseDescription: str):
    prompt_payload = {"courseName": courseName, "courseDescription": courseDescription}
    try:
        response = gemini_client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS_FOR_QUIZ,
            response_mime_type="application/json",
            response_schema=Quiz,
        ),
        contents=json.dumps(prompt_payload),
    )
    except Exception as e:
        if "quota" in str(e):
            raise HTTPException(status_code=500,detail='Gemini API Token Exceeded')
        raise HTTPException(status_code=500,detail='Some different error in AI Layer')

    if response.parsed:
        return response.parsed.model_dump()
    if not response.text:
        raise HTTPException(status_code=500,detail="Gemini returned an empty response")
    print(response.text)
    return _parse_json_response(response.text)
