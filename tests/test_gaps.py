from ml.job_parser import analyze_job
from ml.matching import build_gaps, match_skills

RESUME = ["Python", "Java", "C", "HTML", "CSS", "JavaScript", "MySQL", "Git", "GitHub", "VS Code"]

JD = """Requirements
- 2+ years of experience in Python and SQL
- Experience with Docker

Nice to have:
- AWS
- Git
"""


def gaps_for(resume, job_text):
    return build_gaps(match_skills(resume, analyze_job(job_text)))


def test_missing_required_skills_are_high():
    assert set(gaps_for(RESUME, JD)["high"]) == {"SQL", "Docker"}


def test_missing_preferred_skills_are_medium():
    assert gaps_for(RESUME, JD)["medium"] == ["AWS"]


def test_strengths_are_matched_skills():
    assert gaps_for(RESUME, JD)["strengths"] == ["Python", "Git"]


def test_no_headings_gaps_are_unranked():
    gaps = gaps_for(RESUME, "We need Python and Docker for this role")
    assert gaps["unranked"] == ["Docker"]
    assert gaps["high"] == []
    assert gaps["medium"] == []


def test_responsibility_only_gap_is_low():
    jd = "Responsibilities:\n- Build models with Docker\nRequirements\n- Python"
    gaps = gaps_for(RESUME, jd)
    assert gaps["low"] == ["Docker"]
    assert gaps["high"] == []


def test_skill_is_listed_only_once():
    gaps = gaps_for(RESUME, "Responsibilities:\n- Use Docker")
    assert gaps["unranked"] == ["Docker"]
    assert gaps["low"] == []


def test_full_required_match_has_no_high_gaps():
    gaps = gaps_for(["Python", "SQL", "Docker"], JD)
    assert gaps["high"] == []
    assert gaps["medium"] == ["AWS", "Git"]
    assert gaps["low"] == []
    assert gaps["unranked"] == []
    assert gaps["strengths"] == ["Python", "SQL", "Docker"]


def test_empty_job_has_no_gaps_and_no_strengths():
    gaps = gaps_for(RESUME, "")
    assert gaps == {"high": [], "medium": [], "low": [], "unranked": [], "strengths": []}