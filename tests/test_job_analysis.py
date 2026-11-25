from ml.job_parser import analyze_job

JD = """About the role
We deploy on Kubernetes.

Responsibilities:
- Build models with TensorFlow

Requirements
- Python and SQL
- Docker

Nice to have:
- Docker
- AWS
"""


def test_required_skills_are_found():
    result = analyze_job(JD)
    assert set(result["required"]) == {"Python", "SQL", "Docker"}


def test_preferred_skills_are_found():
    result = analyze_job(JD)
    assert result["preferred"] == ["AWS"]


def test_skill_in_both_sections_counts_as_required_only():
    result = analyze_job(JD)
    assert "Docker" in result["required"]
    assert "Docker" not in result["preferred"]


def test_responsibility_skills_are_kept_separate():
    result = analyze_job(JD)
    assert result["in_responsibilities"] == ["TensorFlow"]
    assert "TensorFlow" not in result["required"]


def test_intro_text_skills_are_ignored_when_headings_exist():
    result = analyze_job(JD)
    all_skills = (
        result["required"] + result["preferred"]
        + result["in_responsibilities"] + result["mentioned"]
    )
    assert "Kubernetes" not in all_skills


def test_no_headings_means_skills_are_only_mentioned():
    result = analyze_job("We need Python and Docker")
    assert result["has_requirement_sections"] is False
    assert result["required"] == []
    assert result["preferred"] == []
    assert set(result["mentioned"]) == {"Python", "Docker"}


def test_empty_job_text_gives_empty_result():
    result = analyze_job("")
    assert result["required"] == []
    assert result["preferred"] == []
    assert result["mentioned"] == []