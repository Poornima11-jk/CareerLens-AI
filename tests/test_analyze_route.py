from io import BytesIO

from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.main import app

client = TestClient(app)
URL = "/api/resume/analyze"


def upload(filename: str, content: bytes):
    return client.post(URL, files={"file": (filename, content, "application/pdf")})


def make_blank_pdf() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    buffer = BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_analyze_returns_detected_and_not_detected(monkeypatch):
    text = "Skills: Python, Git, GitHub"
    monkeypatch.setattr("app.routes.resume.extract_text_from_pdf", lambda data: text)

    response = upload("resume.pdf", b"%PDF-fake")
    body = response.json()

    assert response.status_code == 200
    assert {s["name"] for s in body["detected"]} == {"Python", "Git", "GitHub"}
    assert "Docker" in body["not_detected"]
    assert body["characters"] == len(text)


def test_analyze_rejects_non_pdf_filename():
    response = upload("resume.txt", b"hello")
    assert response.status_code == 400


def test_analyze_rejects_fake_pdf():
    response = upload("resume.pdf", b"not really a pdf")
    assert response.status_code == 400
    assert "valid PDF" in response.json()["detail"]


def test_analyze_rejects_pdf_without_text():
    response = upload("resume.pdf", make_blank_pdf())
    assert response.status_code == 400
    assert "No text detected" in response.json()["detail"]