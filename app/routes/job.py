from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ml.job_parser import analyze_job
from ml.job_requirements import extract_education, extract_experience

MAX_JOB_CHARS = 20000
MIN_JOB_CHARS = 30

router = APIRouter(prefix="/api/job", tags=["job"])


class JobRequest(BaseModel):
    text: str


@router.post("/analyze")
def analyze_job_description(request: JobRequest):
    text = request.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Please paste a job description.")
    if len(text) < MIN_JOB_CHARS:
        raise HTTPException(
            status_code=400,
            detail="The job description is too short to analyze. Please paste the full text.",
        )
    if len(text) > MAX_JOB_CHARS:
        raise HTTPException(
            status_code=400,
            detail="The job description is too long. Maximum is 20,000 characters.",
        )

    skills = analyze_job(text)
    return {
        "characters": len(text),
        "skills": skills,
        "experience": extract_experience(text),
        "education": extract_education(text),
    }