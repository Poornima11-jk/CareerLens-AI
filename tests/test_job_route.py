from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
URL = "/api/job/analyze"

JD = """Requirements
- 3+ years of experience in Python and SQL
- Bachelor's degree in Computer Science

Nice to have:
- Docker
"""


def test_job_analysis_returns_all_parts():
    response = client.post(URL, json={"text": JD})
    body = response.json()

    assert response.status_code == 200
    assert set(body["skills"]["required"]) == {"Python", "SQL"}
    assert body["skills"]["preferred"] == ["Docker"]
    assert body["experience"]["matches"][0]["min_years"] == 3
    assert body["education"]["levels"] == ["Bachelor's"]
    assert body["characters"] == len(JD.strip())


def test_empty_job_text_is_rejected():
    response = client.post(URL, json={"text": "   "})
    assert response.status_code == 400
    assert "paste" in response.json()["detail"]


def test_very_short_job_text_is_rejected():
    response = client.post(URL, json={"text": "Python"})
    assert response.status_code == 400
    assert "too short" in response.json()["detail"]


def test_very_long_job_text_is_rejected():
    response = client.post(URL, json={"text": "a" * 20001})
    assert response.status_code == 400
    assert "too long" in response.json()["detail"]


def test_missing_text_field_is_rejected():
    response = client.post(URL, json={})
    assert response.status_code == 422


def test_job_page_loads():
    response = client.get("/job")
    assert response.status_code == 200
    assert "Add a job description" in response.text