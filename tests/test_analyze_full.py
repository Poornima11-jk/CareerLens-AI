from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
URL = "/api/analyze"

JD = """Requirements
- 2+ years of experience in Python and SQL
- Experience with Docker

Nice to have:
- AWS
- Git
"""


def post(job_text, resume_bytes=b"%PDF-fake"):
    return client.post(
        URL,
        files={"file": ("resume.pdf", resume_bytes, "application/pdf")},
        data={"job_text": job_text},
    )


def fake_resume(monkeypatch, text="Skills: Python, Java, C, Git"):
    monkeypatch.setattr("app.routes.resume.extract_text_from_pdf", lambda data: text)


def test_full_analysis_numbers(monkeypatch):
    fake_resume(monkeypatch)
    body = post(JD).json()

    assert set(body["resume_skills"]) == {"Python", "Java", "C", "Git"}
    assert body["score"]["required_match"] == 33
    assert body["score"]["preferred_match"] == 50
    assert body["score"]["overall"] == 37          # 0.8*33.3 + 0.2*50
    assert set(body["gaps"]["high"]) == {"SQL", "Docker"}
    assert body["gaps"]["medium"] == ["AWS"]
    assert body["gaps"]["strengths"] == ["Python", "Git"]
    assert body["experience"]["matches"][0]["min_years"] == 2


def test_blank_job_text_is_rejected(monkeypatch):
    fake_resume(monkeypatch)
    response = post("   ")
    assert response.status_code == 400
    assert "paste" in response.json()["detail"]


def test_short_job_text_is_rejected(monkeypatch):
    fake_resume(monkeypatch)
    response = post("Python")
    assert response.status_code == 400
    assert "too short" in response.json()["detail"]


def test_bad_resume_is_rejected():
    response = post(JD, resume_bytes=b"not a pdf")
    assert response.status_code == 400
    assert "valid PDF" in response.json()["detail"]


def test_missing_job_text_field_is_rejected():
    response = client.post(
        URL, files={"file": ("resume.pdf", b"%PDF-x", "application/pdf")}
    )
    assert response.status_code == 422


def test_analyze_page_loads():
    response = client.get("/analyze")
    assert response.status_code == 200
    assert "Full analysis" in response.text