import json
import re
from functools import lru_cache
from pathlib import Path

from ml.preprocessing import normalize_for_matching

SKILLS_FILE = Path(__file__).resolve().parent / "skills.json"


@lru_cache(maxsize=1)
def load_skills() -> list:
    data = json.loads(SKILLS_FILE.read_text(encoding="utf-8"))
    return data["skills"]


def _term_pattern(term: str) -> re.Pattern:
    return re.compile(r"(?<![a-z0-9+#.])" + re.escape(term) + r"(?![a-z0-9+#])")


def extract_skills(text: str) -> dict:
    normalized = normalize_for_matching(text)
    detected = []
    not_detected = []

    for skill in load_skills():
        terms = [normalize_for_matching(skill["name"])] + skill["aliases"]
        found = [term for term in terms if _term_pattern(term).search(normalized)]
        if found:
            detected.append(
                {
                    "name": skill["name"],
                    "category": skill["category"],
                    "matched_as": found,
                }
            )
        else:
            not_detected.append(skill["name"])

    return {"detected": detected, "not_detected": not_detected}