from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings

gemini_client = genai.Client(api_key=settings.gemini_api_key)

gemini_embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    api_key=settings.gemini_api_key,
    output_dimensionality=768,
)
