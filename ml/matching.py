def _split(wanted: list, have: set) -> tuple:
    matched = [name for name in wanted if name in have]
    missing = [name for name in wanted if name not in have]
    return matched, missing


def match_skills(resume_skills: list, job_skills: dict) -> dict:
    have = set(resume_skills)

    matched_required, missing_required = _split(job_skills["required"], have)
    matched_preferred, missing_preferred = _split(job_skills["preferred"], have)
    matched_mentioned, missing_mentioned = _split(job_skills["mentioned"], have)
    matched_resp, missing_resp = _split(job_skills["in_responsibilities"], have)

    asked_for = set(
        job_skills["required"]
        + job_skills["preferred"]
        + job_skills["mentioned"]
        + job_skills["in_responsibilities"]
    )
    extra_skills = [name for name in resume_skills if name not in asked_for]

    return {
        "has_requirement_sections": job_skills["has_requirement_sections"],
        "required": {"matched": matched_required, "missing": missing_required},
        "preferred": {"matched": matched_preferred, "missing": missing_preferred},
        "mentioned": {"matched": matched_mentioned, "missing": missing_mentioned},
        "responsibilities": {"matched": matched_resp, "missing": missing_resp},
        "extra_skills": extra_skills,
    }
REQUIRED_WEIGHT = 0.8
PREFERRED_WEIGHT = 0.2


def _ratio(group: dict):
    total = len(group["matched"]) + len(group["missing"])
    if total == 0:
        return None
    return len(group["matched"]) / total


def _percent(value):
    return None if value is None else round(value * 100)


def calculate_score(match: dict) -> dict:
    required = _ratio(match["required"])
    preferred = _ratio(match["preferred"])
    mentioned = _ratio(match["mentioned"])

    if required is not None and preferred is not None:
        overall = REQUIRED_WEIGHT * required + PREFERRED_WEIGHT * preferred
        method = "80% required + 20% preferred"
    elif required is not None:
        overall = required
        method = "required skills only (no preferred skills found)"
    elif preferred is not None:
        overall = preferred
        method = "preferred skills only (no required skills found)"
    elif mentioned is not None:
        overall = mentioned
        method = "all mentioned skills (job had no headings, so required and preferred are unknown)"
    else:
        overall = None
        method = "no score: no recognised skills in the job description"

    return {
        "overall": _percent(overall),
        "required_match": _percent(required),
        "preferred_match": _percent(preferred),
        "mentioned_match": _percent(mentioned),
        "method": method,
        "weights": {"required": REQUIRED_WEIGHT, "preferred": PREFERRED_WEIGHT},
    }
def build_gaps(match: dict) -> dict:
    high = list(match["required"]["missing"])
    medium = [n for n in match["preferred"]["missing"] if n not in high]
    unranked = [
        n for n in match["mentioned"]["missing"]
        if n not in high and n not in medium
    ]
    low = [
        n for n in match["responsibilities"]["missing"]
        if n not in high and n not in medium and n not in unranked
    ]

    strengths = []
    for group in ("required", "preferred", "mentioned", "responsibilities"):
        for name in match[group]["matched"]:
            if name not in strengths:
                strengths.append(name)

    return {
        "high": high,
        "medium": medium,
        "low": low,
        "unranked": unranked,
        "strengths": strengths,
    }