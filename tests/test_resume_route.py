from io import BytesIO

from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.main import app

client = TestClient(app)
URL = "/api/resume/extract-text"


def upload(filename: str, content: bytes):
    return client.post(URL, files={"file": (filename, content, "application/pdf")})


def make_blank_pdf() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    buffer = BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_non_pdf_filename_is_rejected():
    response = upload("resume.txt", b"hello")
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_empty_file_is_rejected():
    response = upload("resume.pdf", b"")
    assert response.status_code == 400
    assert "empty" in response.json()["detail"]


def test_fake_pdf_is_rejected():
    response = upload("resume.pdf", b"this is not really a pdf")
    assert response.status_code == 400
    assert "valid PDF" in response.json()["detail"]


def test_pdf_without_text_is_rejected():
    response = upload("resume.pdf", make_blank_pdf())
    assert response.status_code == 400
    assert "No text detected" in response.json()["detail"]