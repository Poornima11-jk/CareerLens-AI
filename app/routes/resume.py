from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.pdf_extractor import (
    MAX_FILE_SIZE_BYTES,
    ResumeError,
    extract_text_from_pdf,
)

router = APIRouter(prefix="/api/resume", tags=["resume"])


@router.post("/extract-text")
async def extract_resume_text(file: UploadFile = File(...)):
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file (.pdf).")

    file_bytes = await file.read(MAX_FILE_SIZE_BYTES + 1)

    try:
        text = extract_text_from_pdf(file_bytes)
    except ResumeError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "filename": filename,
        "characters": len(text),
        "preview": text[:500],
    }