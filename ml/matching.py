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