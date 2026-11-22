from ml.preprocessing import clean_text, normalize_for_matching


def test_clean_text_collapses_extra_spaces():
    assert clean_text("Python     and   SQL") == "Python and SQL"


def test_clean_text_removes_bullet_symbols():
    assert clean_text("• Python\n▪ SQL") == "Python\nSQL"


def test_clean_text_limits_blank_lines():
    assert clean_text("A\n\n\n\nB") == "A\n\nB"


def test_normalize_lowercases_and_removes_punctuation():
    text = "Programming: Python, Java, C (beginner to intermediate)"
    expected = "programming python java c beginner to intermediate"
    assert normalize_for_matching(text) == expected


def test_normalize_keeps_skill_symbols():
    result = normalize_for_matching("C++ and C# developer, Node.js, CI/CD")
    assert result == "c++ and c# developer node.js ci/cd"


def test_normalize_removes_trailing_dots():
    assert normalize_for_matching("Git. GitHub.") == "git github"


def test_empty_text_returns_empty_string():
    assert clean_text("") == ""
    assert normalize_for_matching("") == ""