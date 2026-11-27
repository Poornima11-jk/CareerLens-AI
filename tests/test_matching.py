from ml.job_parser import analyze_job
from ml.matching import match_skills

RESUME = ["Python", "Java", "C", "HTML", "CSS", "JavaScript", "MySQL", "Git", "GitHub", "VS Code"]

JD = """Requirements
- 2+ years of experience in Python and SQL
- Experience with Docker

Nice to have:
- AWS
- Git
"""


def test_required_matched_and_missing():
    result = match_skills(RESUME, analyze_job(JD))
    assert result["required"]["matched"] == ["Python"]
    assert set(result["required"]["missing"]) == {"SQL", "Docker"}


def test_preferred_matched_and_missing():
    result = match_skills(RESUME, analyze_job(JD))
    assert result["preferred"]["matched"] == ["Git"]
    assert result["preferred"]["missing"] == ["AWS"]


def test_mysql_does_not_count_as_sql():
    result = match_skills(RESUME, analyze_job(JD))
    assert "SQL" in result["required"]["missing"]


def test_extra_skills_are_resume_skills_the_job_did_not_ask_for():
    result = match_skills(RESUME, analyze_job(JD))
    assert "Java" in result["extra_skills"]
    assert "Python" not in result["extra_skills"]
    assert "Git" not in result["extra_skills"]


def test_no_headings_uses_mentioned_group():
    result = match_skills(RESUME, analyze_job("We need Python and Docker for this role"))
    assert result["has_requirement_sections"] is False
    assert result["mentioned"]["matched"] == ["Python"]
    assert result["mentioned"]["missing"] == ["Docker"]
    assert result["required"] == {"matched": [], "missing": []}


def test_responsibility_skills_are_reported_separately():
    jd = "Responsibilities:\n- Build models with Docker\nRequirements\n- Python"
    result = match_skills(RESUME, analyze_job(jd))
    assert result["responsibilities"]["missing"] == ["Docker"]
    assert result["required"]["matched"] == ["Python"]


def test_empty_resume_matches_nothing():
    result = match_skills([], analyze_job(JD))
    assert result["required"]["matched"] == []
    assert set(result["required"]["missing"]) == {"Python", "SQL", "Docker"}
    assert result["extra_skills"] == []


def test_empty_job_gives_empty_groups():
    result = match_skills(RESUME, analyze_job(""))
    assert result["required"] == {"matched": [], "missing": []}
    assert result["mentioned"] == {"matched": [], "missing": []}
    assert result["extra_skills"] == RESUME