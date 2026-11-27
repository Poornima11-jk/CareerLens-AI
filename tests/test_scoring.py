from ml.matching import calculate_score


def group(matched, missing):
    return {"matched": matched, "missing": missing}


def build(required=None, preferred=None, mentioned=None):
    empty = group([], [])
    return {
        "required": required or empty,
        "preferred": preferred or empty,
        "mentioned": mentioned or empty,
    }


def test_required_and_preferred_are_weighted():
    match = build(
        required=group(["a", "b"], ["c", "d"]),   # 50%
        preferred=group(["x"], []),               # 100%
    )
    score = calculate_score(match)
    assert score["required_match"] == 50
    assert score["preferred_match"] == 100
    assert score["overall"] == 60                 # 0.8*50 + 0.2*100
    assert score["method"] == "80% required + 20% preferred"


def test_worked_example_from_lesson():
    match = build(
        required=group(["Python"], ["SQL", "Docker"]),
        preferred=group([], ["AWS", "Kubernetes"]),
    )
    score = calculate_score(match)
    assert score["required_match"] == 33
    assert score["preferred_match"] == 0
    assert score["overall"] == 27


def test_required_only_uses_required_alone():
    score = calculate_score(build(required=group(["a"], ["b"])))
    assert score["overall"] == 50
    assert score["preferred_match"] is None


def test_preferred_only_uses_preferred_alone():
    score = calculate_score(build(preferred=group(["a"], ["b", "c", "d"])))
    assert score["overall"] == 25
    assert score["required_match"] is None


def test_mentioned_only_when_no_headings():
    score = calculate_score(build(mentioned=group(["a", "b"], ["c"])))
    assert score["overall"] == 67
    assert "no headings" in score["method"]


def test_no_skills_gives_no_score_not_zero_or_hundred():
    score = calculate_score(build())
    assert score["overall"] is None
    assert "no score" in score["method"]


def test_perfect_match_is_100():
    score = calculate_score(build(required=group(["a", "b"], [])))
    assert score["overall"] == 100


def test_no_match_is_0_when_skills_exist():
    score = calculate_score(build(required=group([], ["a", "b"])))
    assert score["overall"] == 0


def test_weights_add_up_to_one():
    weights = calculate_score(build())["weights"]
    assert weights["required"] + weights["preferred"] == 1