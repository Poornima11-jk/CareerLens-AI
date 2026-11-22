from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.pdf_extractor import (
    MAX_FILE_SIZE_BYTES,
    ResumeError,
    extract_text_from_pdf,
)
from ml.skill_extraction import extract_skills

router = APIRouter(prefix="/api/resume", tags=["resume"])


async def read_resume_text(file: UploadFile) -> tuple[str, str]:
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file (.pdf).")

    file_bytes = await file.read(MAX_FILE_SIZE_BYTES + 1)

    try:
        text = extract_text_from_pdf(file_bytes)
    except ResumeError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return filename, text


@router.post("/extract-text")
async def extract_resume_text(file: UploadFile = File(...)):
    filename, text = await read_resume_text(file)
    return {
        "filename": filename,
        "characters": len(text),
        "preview": text[:500],
    }


@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    filename, text = await read_resume_text(file)
    skills = extract_skills(text)
    return {
        "filename": filename,
        "characters": len(text),
        "detected": skills["detected"],
        "not_detected": skills["not_detected"],
    }