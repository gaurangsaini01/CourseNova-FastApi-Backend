from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

from app.core.config import settings


def get_qdrant_client():
    return QdrantClient(
        url=settings.qdrant_api_url,
        api_key=settings.qdrant_api_key,
    )


def ensure_payload_indexes():
    client = get_qdrant_client()
    index_fields = [
        "metadata.course_id",
        "metadata.subsection_id",
        "metadata.source_type",
    ]

    for field_name in index_fields:
        client.create_payload_index(
            collection_name=settings.qdrant_collection_name,
            field_name=field_name,
            field_schema=models.PayloadSchemaType.KEYWORD,
            wait=True,
        )


def store_documents_in_qdrant(documents, embeddings):
    vector_db = QdrantVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=settings.qdrant_collection_name,
        url=settings.qdrant_api_url,
        api_key=settings.qdrant_api_key,
    )
    ensure_payload_indexes()
    return vector_db


def get_qdrant_vector_store(embeddings):
    ensure_payload_indexes()
    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=settings.qdrant_collection_name,
        url=settings.qdrant_api_url,
        api_key=settings.qdrant_api_key,
    )


def delete_documents_from_qdrant(delete_filter):
    client = get_qdrant_client()
    ensure_payload_indexes()
    return client.delete(
        collection_name=settings.qdrant_collection_name,
        points_selector=delete_filter,
        wait=True,
    )
