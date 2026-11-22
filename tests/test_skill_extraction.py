from ml.skill_extraction import extract_skills, load_skills


def detected_names(text: str) -> set:
    return {skill["name"] for skill in extract_skills(text)["detected"]}


def test_sample_resume_skills_line():
    text = (
        "TECHNICAL SKILLS Programming: Python, Java, C (beginner to intermediate) "
        "Web: HTML, CSS, JavaScript basics Database: MySQL Tools: VS Code, Git, GitHub"
    )
    assert detected_names(text) == {
        "Python", "Java", "C", "HTML", "CSS", "JavaScript",
        "MySQL", "VS Code", "Git", "GitHub",
    }


def test_letter_c_inside_words_is_not_detected():
    names = detected_names("I live in Chennai and write python")
    assert "C" not in names
    assert "Python" in names


def test_cpp_does_not_detect_c():
    names = detected_names("I know C++")
    assert "C++" in names
    assert "C" not in names


def test_csharp_does_not_detect_c():
    names = detected_names("I know C#")
    assert "C#" in names
    assert "C" not in names


def test_javascript_does_not_detect_java():
    names = detected_names("JavaScript")
    assert "JavaScript" in names
    assert "Java" not in names


def test_mysql_does_not_detect_sql():
    names = detected_names("MySQL")
    assert "MySQL" in names
    assert "SQL" not in names


def test_github_does_not_detect_git():
    names = detected_names("GitHub")
    assert "GitHub" in names
    assert "Git" not in names


def test_alias_is_detected_and_reported():
    result = extract_skills("ML projects")
    skill = next(s for s in result["detected"] if s["name"] == "Machine Learning")
    assert skill["matched_as"] == ["ml"]


def test_nodejs_does_not_detect_javascript_alias():
    names = detected_names("Node.js")
    assert "Node.js" in names
    assert "JavaScript" not in names


def test_ordinary_word_rest_is_not_rest_api():
    assert "REST API" not in detected_names("I will handle the rest of the team")


def test_matching_ignores_capitals():
    assert "Python" in detected_names("PYTHON")


def test_slash_separated_skills_are_both_detected():
    assert {"HTML", "CSS"} <= detected_names("HTML/CSS")


def test_empty_text_detects_nothing():
    result = extract_skills("")
    assert result["detected"] == []
    assert len(result["not_detected"]) == len(load_skills())