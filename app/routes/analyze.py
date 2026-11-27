from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.routes.job import MAX_JOB_CHARS, MIN_JOB_CHARS
from app.routes.resume import read_resume_text
from ml.job_parser import analyze_job
from ml.job_requirements import extract_education, extract_experience
from ml.matching import build_gaps, calculate_score, match_skills
from ml.skill_extraction import extract_skills

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze")
async def analyze(file: UploadFile = File(...), job_text: str = Form(...)):
    filename, resume_text = await read_resume_text(file)

    job = job_text.strip()
    if not job:
        raise HTTPException(status_code=400, detail="Please paste a job description.")
    if len(job) < MIN_JOB_CHARS:
        raise HTTPException(
            status_code=400,
            detail="The job description is too short to analyze. Please paste the full text.",
        )
    if len(job) > MAX_JOB_CHARS:
        raise HTTPException(
            status_code=400,
            detail="The job description is too long. Maximum is 20,000 characters.",
        )

    resume_skills = [s["name"] for s in extract_skills(resume_text)["detected"]]
    job_skills = analyze_job(job)
    match = match_skills(resume_skills, job_skills)

    return {
        "filename": filename,
        "resume_skills": resume_skills,
        "score": calculate_score(match),
        "match": match,
        "gaps": build_gaps(match),
        "experience": extract_experience(job),
        "education": extract_education(job),
    }