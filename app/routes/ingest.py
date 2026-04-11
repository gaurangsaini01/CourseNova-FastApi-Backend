import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.core.security import check_secret_key
from app.services.ingestion import (
    delete_pdf_ingestion,
    ingest_pdf as ingest_pdf_documents,
)

router = APIRouter()


@router.post("/ingestPdf")
def ingest_pdf(
    notesPdf: UploadFile = File(...),
    course: str = Form(...),
    subSection: str = Form(...),
    _: None = Depends(check_secret_key),
):
    try:
        parsed_course = json.loads(course)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid course payload. Send course as JSON.stringify(course).",
        ) from exc
    try:
        parsed_subsection = json.loads(subSection)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid subSection payload. Send subSection as JSON.stringify(subSection).",
        ) from exc
    ingestion_response = ingest_pdf_documents(
        notesPdf,
        parsed_course,
        parsed_subsection,
    )
    return {"success": True, "documentsCount": len(ingestion_response)}


@router.post("/deletePdfIngestion")
def delete_pdf_ingestion_endpoint(
    course: str = Form(...),
    subSection: str = Form(...),
    _: None = Depends(check_secret_key),
):
    try:
        parsed_course = json.loads(course)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid course payload. Send course as JSON.stringify(course).",
        ) from exc

    try:
        parsed_subsection = json.loads(subSection)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid subSection payload. Send subSection as JSON.stringify(subSection).",
        ) from exc

    delete_response = delete_pdf_ingestion(parsed_course, parsed_subsection)
    return {"success": True, "deleteResponse": delete_response.model_dump()}
