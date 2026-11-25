import re

from ml.preprocessing import clean_text

_YEARS = re.compile(
    r"(?<![\d.])(\d{1,2})\s*(\+)?\s*"
    r"(?:(?:-|\u2013|\u2014|to)\s*(\d{1,2})\s*(\+)?\s*)?"
    r"(?:years?|yrs?)\b",
    re.IGNORECASE,
)
_EXPERIENCE_WORD = re.compile(r"experience", re.IGNORECASE)
_ENTRY_LEVEL = re.compile(
    r"\bfreshers?\b|\bentry[- ]level\b"
    r"|\bno (?:prior )?experience (?:is )?(?:required|needed|necessary)\b"
)

EDUCATION_LEVELS = [
    ("Diploma", [r"diploma"]),
    ("Bachelor's", [
        r"bachelor'?s?", r"b\.?tech", r"b\.e\.", r"b\.?sc", r"bca",
        r"under[- ]?graduate",
    ]),
    ("Master's", [
        r"master'?s", r"master\s+(?:of|degree)", r"m\.?tech", r"m\.?sc",
        r"mca", r"post[- ]?graduate",
    ]),
    ("PhD", [r"ph\.?d", r"doctorate", r"doctoral"]),
]


def _word_pattern(alternatives: list) -> re.Pattern:
    return re.compile(r"(?<![a-z0-9])(?:" + "|".join(alternatives) + r")(?![a-z0-9])")


_LEVEL_PATTERNS = [(name, _word_pattern(alts)) for name, alts in EDUCATION_LEVELS]
_DEGREE_WORD = _word_pattern([r"degrees?"])


def _prepare(text: str) -> str:
    return clean_text(text).replace("\u2019", "'")


def extract_experience(text: str) -> dict:
    cleaned = _prepare(text)
    matches = []

    for line in cleaned.splitlines():
        if not _EXPERIENCE_WORD.search(line):
            continue
        for found in _YEARS.finditer(line):
            matches.append(
                {
                    "text": found.group(0).strip(),
                    "min_years": int(found.group(1)),
                    "max_years": int(found.group(3)) if found.group(3) else None,
                    "line": line,
                }
            )

    return {
        "matches": matches,
        "entry_level": bool(_ENTRY_LEVEL.search(cleaned.lower())),
    }


def extract_education(text: str) -> dict:
    lowered = _prepare(text).lower()
    levels = [name for name, pattern in _LEVEL_PATTERNS if pattern.search(lowered)]
    return {
        "levels": levels,
        "degree_mentioned": bool(_DEGREE_WORD.search(lowered)),
    }