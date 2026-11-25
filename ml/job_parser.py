from ml.preprocessing import clean_text
from ml.skill_extraction import extract_skills
HEADING_PHRASES = {
    "required": [
        "requirements", "requirement", "required", "required skills",
        "required qualifications", "required skills and qualifications",
        "qualifications", "minimum qualifications", "basic qualifications",
        "must have", "must-have", "must haves", "what you need",
        "what you'll need", "what we're looking for", "skills required",
        "key skills", "skills and qualifications", "skills & qualifications",
    ],
    "preferred": [
        "preferred", "preferred skills", "preferred qualifications",
        "nice to have", "nice-to-have", "good to have", "good-to-have",
        "bonus", "bonus points", "desirable", "desired skills",
        "additional skills", "added advantage",
    ],
    "responsibilities": [
        "responsibilities", "key responsibilities", "your responsibilities",
        "roles and responsibilities", "role and responsibilities",
        "what you will do", "what you'll do", "duties", "job duties",
    ],
    "other": [
        "about us", "about the company", "about the role", "about the job",
        "job description", "overview", "company overview", "job summary",
        "summary", "benefits", "what we offer", "perks", "who we are",
        "equal opportunity",
    ],
}

HEADINGS = {
    phrase: section
    for section, phrases in HEADING_PHRASES.items()
    for phrase in phrases
}


def _match_heading(line: str):
    head, _, rest = line.partition(":")
    key = head.strip().lower().replace("\u2019", "'")
    if key in HEADINGS:
        return HEADINGS[key], rest.strip()
    return None


def split_job_sections(text: str) -> dict:
    buckets = {"required": [], "preferred": [], "responsibilities": [], "other": []}
    current = "other"
    found_requirement_heading = False

    for line in clean_text(text).splitlines():
        match = _match_heading(line)
        if match:
            current, rest = match
            if current in ("required", "preferred"):
                found_requirement_heading = True
            if rest:
                buckets[current].append(rest)
        elif line:
            buckets[current].append(line)

    result = {name: "\n".join(lines) for name, lines in buckets.items()}
    result["has_requirement_sections"] = found_requirement_heading
    return result
def _names(text: str) -> list:
    return [skill["name"] for skill in extract_skills(text)["detected"]]


def analyze_job(text: str) -> dict:
    sections = split_job_sections(text)

    if sections["has_requirement_sections"]:
        required = _names(sections["required"])
        preferred = [n for n in _names(sections["preferred"]) if n not in required]
        mentioned = []
    else:
        required = []
        preferred = []
        mentioned = _names(text)

    in_responsibilities = [
        n for n in _names(sections["responsibilities"])
        if n not in required and n not in preferred
    ]

    return {
        "has_requirement_sections": sections["has_requirement_sections"],
        "required": required,
        "preferred": preferred,
        "in_responsibilities": in_responsibilities,
        "mentioned": mentioned,
    }