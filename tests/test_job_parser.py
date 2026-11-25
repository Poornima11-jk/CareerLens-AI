from ml.job_parser import HEADING_PHRASES, HEADINGS, split_job_sections

SAMPLE_JD = """About the role
We build ML products.

Responsibilities:
- Build and deploy models
- Write clean code

Requirements
- Python and SQL
- 2+ years experience

Nice to have:
- Docker
- Kubernetes
"""


def test_required_section_is_found():
    sections = split_job_sections(SAMPLE_JD)
    assert "Python and SQL" in sections["required"]
    assert "Docker" not in sections["required"]


def test_preferred_section_is_found():
    sections = split_job_sections(SAMPLE_JD)
    assert "Docker" in sections["preferred"]
    assert "Python" not in sections["preferred"]


def test_responsibilities_section_is_found():
    sections = split_job_sections(SAMPLE_JD)
    assert "Build and deploy models" in sections["responsibilities"]


def test_intro_text_goes_to_other():
    sections = split_job_sections(SAMPLE_JD)
    assert "We build ML products." in sections["other"]


def test_requirement_headings_are_reported():
    assert split_job_sections(SAMPLE_JD)["has_requirement_sections"] is True


def test_text_on_the_same_line_as_heading_is_kept():
    sections = split_job_sections("Requirements: Python, SQL")
    assert sections["required"] == "Python, SQL"


def test_heading_ignores_capitals_and_curly_apostrophe():
    sections = split_job_sections("WHAT YOU\u2019LL NEED\nPython")
    assert sections["required"] == "Python"


def test_text_without_headings_is_not_split():
    sections = split_job_sections("We need Python")
    assert sections["has_requirement_sections"] is False
    assert sections["required"] == ""
    assert "We need Python" in sections["other"]


def test_sentence_with_colon_is_not_a_heading():
    sections = split_job_sections("Experience with Python: 2 years")
    assert sections["has_requirement_sections"] is False
    assert "Experience with Python: 2 years" in sections["other"]


def test_benefits_heading_ends_the_preferred_section():
    sections = split_job_sections("Nice to have\nDocker\nBenefits\nFree lunch")
    assert "Free lunch" not in sections["preferred"]
    assert "Free lunch" in sections["other"]


def test_empty_text_gives_empty_sections():
    sections = split_job_sections("")
    assert sections["required"] == ""
    assert sections["preferred"] == ""
    assert sections["has_requirement_sections"] is False


def test_heading_list_has_no_duplicates_and_is_lowercase():
    total = sum(len(phrases) for phrases in HEADING_PHRASES.values())
    assert total == len(HEADINGS)
    assert all(phrase == phrase.lower() for phrase in HEADINGS)