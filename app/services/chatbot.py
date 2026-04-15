from qdrant_client import models
import json
from app.core.clients import openai_client, openai_embeddings
from app.core.qdrant import get_qdrant_vector_store
from app.core.system_instructions import SYSTEM_INSTRUCTIONS_FOR_CHATBOT

# from google.genai import types
from app.schemas.chatbot import ChatBotSchema
from fastapi import HTTPException


def ask_query_from_chatbot(query: str, course_id: str):
    vector_store = get_qdrant_vector_store(openai_embeddings)
    course_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.course_id",
                match=models.MatchValue(value=course_id),
            )
        ]
    )

    results = vector_store.similarity_search(
        query=query,
        k=3,
        filter=course_filter,
    )
    prompt_payload = {
        "query": query,
        "context": [
            {
                "page_content": result.page_content,
                "metadata": result.metadata,
            }
            for result in results
        ],
    }

    try:
        response = openai_client.responses.parse(
            model="gpt-5.4-mini",
            text_format=ChatBotSchema,
            instructions=SYSTEM_INSTRUCTIONS_FOR_CHATBOT,
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
        raise HTTPException(status_code=500, detail="OpenAI returned an empty response")

    return response.output_parsed
