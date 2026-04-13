from qdrant_client import models
import json
from app.core.clients import gemini_embeddings, gemini_client
from app.core.qdrant import get_qdrant_vector_store
from app.core.system_instructions import SYSTEM_INSTRUCTIONS_FOR_CHATBOT
from google.genai import types
from app.schemas.chatbot import ChatBotSchema
from fastapi import HTTPException

def ask_query_from_chatbot(query: str, course_id: str):
    vector_store = get_qdrant_vector_store(gemini_embeddings)
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
        response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS_FOR_CHATBOT,
            response_mime_type="application/json",
            response_schema=ChatBotSchema,
        ),
        contents=json.dumps(prompt_payload),
    )
    except Exception as e:
        if 'quota' in str(e):
            raise HTTPException(status_code=500,detail='AI CREDITS EXHAUSTED')
        raise HTTPException(status_code=500,detail='Service layer Issue')
        
    if response.parsed:
        return response.parsed.model_dump()

    return response.text
