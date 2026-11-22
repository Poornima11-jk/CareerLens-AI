from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_page_loads():
    response = client.get("/upload")
    assert response.status_code == 200
    assert "Upload your resume" in response.text