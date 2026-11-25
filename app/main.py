from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes.job import router as job_router
from app.routes.resume import router as resume_router

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="CareerLens AI",
    description="AI-Powered Career & Skill Gap Analyzer",
    version="0.1.0",
)

app.include_router(resume_router)
app.include_router(job_router)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")


@app.get("/", include_in_schema=False)
def landing_page():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/upload", include_in_schema=False)
def upload_page():
    return FileResponse(FRONTEND_DIR / "upload.html")


@app.get("/job", include_in_schema=False)
def job_page():
    return FileResponse(FRONTEND_DIR / "job.html")


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "CareerLens AI", "version": "0.1.0"}


@app.get("/version")
def version():
    return {"version": "0.1.0"}