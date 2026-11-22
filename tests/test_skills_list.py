import json
from pathlib import Path

from ml.preprocessing import normalize_for_matching

SKILLS_FILE = Path(__file__).resolve().parent.parent / "ml" / "skills.json"


def load_skills():
    return json.loads(SKILLS_FILE.read_text(encoding="utf-8"))["skills"]


def test_skills_file_loads_and_is_not_empty():
    assert len(load_skills()) > 0


def test_every_skill_has_name_category_and_aliases():
    for skill in load_skills():
        assert skill["name"].strip()
        assert skill["category"].strip()
        assert isinstance(skill["aliases"], list)


def test_all_terms_are_already_normalized():
    for skill in load_skills():
        terms = [skill["name"]] + skill["aliases"]
        for term in terms:
            assert normalize_for_matching(term) == term.lower(), term


def test_no_term_belongs_to_two_skills():
    owner = {}
    for skill in load_skills():
        terms = [normalize_for_matching(skill["name"])] + skill["aliases"]
        for term in terms:
            assert term not in owner, f"{term!r} is used by {owner.get(term)} and {skill['name']}"
            owner[term] = skill["name"]


def test_skills_from_sample_resume_are_in_list():
    names = {skill["name"] for skill in load_skills()}
    sample = {"Python", "Java", "C", "HTML", "CSS", "JavaScript", "MySQL", "Git", "GitHub", "VS Code"}
    assert sample <= names