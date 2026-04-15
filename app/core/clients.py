from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
from openai import OpenAI

openai_client = OpenAI(api_key=settings.openai_api_key)

openai_embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=settings.openai_api_key
)