import io

from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import models

from app.core.clients import openai_embeddings
from app.core.qdrant import delete_documents_from_qdrant, store_documents_in_qdrant


def ingest_pdf(notes_pdf, course, sub_section):
    pdf_bytes = notes_pdf.file.read()
    pdf_buffer = io.BytesIO(pdf_bytes)
    reader = PdfReader(pdf_buffer)
    pages = reader.pages
    docs = []
    total_pages = len(pages)

    base_metadata = {
        "course_id": course.get("_id"),
        "course_name": course.get("courseName"),
        "course_description": course.get("courseDescription"),
        "category": course.get("category"),
        "subsection_id": sub_section.get("_id"),
        "subsection_name":sub_section.get('title'),
        "document_name": notes_pdf.filename,
        "source_type": "notes_pdf",
        "total_pages": total_pages,
    }

    for i, page in enumerate(pages):
        raw_text = page.extract_text() or ""
        if raw_text.strip():
            docs.append(
                Document(
                    page_content=raw_text,
                    metadata={
                        **base_metadata,
                        "page_number": i + 1,
                    },
                )
            )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
    )
    chunked_docs = text_splitter.split_documents(docs)

    for index, chunk in enumerate(chunked_docs):
        chunk.metadata["chunk_index"] = index

    if chunked_docs:
        store_documents_in_qdrant(chunked_docs, openai_embeddings)

    return chunked_docs


def delete_pdf_ingestion(course, sub_section):
    delete_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.course_id",
                match=models.MatchValue(value=course.get("_id")),
            ),
            models.FieldCondition(
                key="metadata.subsection_id",
                match=models.MatchValue(value=sub_section.get("_id")),
            ),
            models.FieldCondition(
                key="metadata.source_type",
                match=models.MatchValue(value="notes_pdf"),
            ),
        ]
    )

    return delete_documents_from_qdrant(delete_filter)
