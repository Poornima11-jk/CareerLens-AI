from ml.job_requirements import extract_education, extract_experience


def first_match(text: str) -> dict:
    return extract_experience(text)["matches"][0]


def test_years_with_plus():
    match = first_match("Minimum 2+ years of experience in Python")
    assert match["text"] == "2+ years"
    assert match["min_years"] == 2
    assert match["max_years"] is None


def test_years_range_with_dash():
    match = first_match("3-5 years experience required")
    assert match["min_years"] == 3
    assert match["max_years"] == 5


def test_years_range_with_to():
    match = first_match("3 to 5 years of experience")
    assert match["min_years"] == 3
    assert match["max_years"] == 5


def test_range_starting_at_zero():
    match = first_match("0-2 years of experience")
    assert match["min_years"] == 0
    assert match["max_years"] == 2


def test_en_dash_range():
    match = first_match("3\u20135 years of experience")
    assert match["min_years"] == 3
    assert match["max_years"] == 5


def test_years_without_experience_word_are_ignored():
    assert extract_experience("Founded 10 years ago")["matches"] == []
    assert extract_experience("We have 10 years in business")["matches"] == []


def test_multiple_experience_lines():
    text = "5+ years of experience in ML\n2 years of experience with Docker"
    matches = extract_experience(text)["matches"]
    assert [m["min_years"] for m in matches] == [5, 2]


def test_no_experience_mentioned():
    result = extract_experience("Python and SQL")
    assert result["matches"] == []
    assert result["entry_level"] is False


def test_fresher_is_entry_level():
    result = extract_experience("Freshers welcome")
    assert result["entry_level"] is True
    assert result["matches"] == []


def test_entry_level_with_hyphen():
    assert extract_experience("Entry-level role")["entry_level"] is True


def test_empty_text_has_no_experience():
    assert extract_experience("") == {"matches": [], "entry_level": False}


def test_bachelor_with_degree_word():
    result = extract_education("Bachelor's degree in Computer Science")
    assert result["levels"] == ["Bachelor's"]
    assert result["degree_mentioned"] is True


def test_curly_apostrophe_is_handled():
    assert extract_education("Bachelor\u2019s degree")["levels"] == ["Bachelor's"]


def test_btech_and_be_count_once():
    assert extract_education("B.Tech or B.E. in CS")["levels"] == ["Bachelor's"]


def test_mtech_and_msc_are_masters():
    assert extract_education("M.Tech/MSc preferred")["levels"] == ["Master's"]


def test_phd_is_detected():
    assert extract_education("PhD in machine learning")["levels"] == ["PhD"]


def test_levels_are_ordered_low_to_high():
    result = extract_education("Bachelor's or Master's degree")
    assert result["levels"] == ["Bachelor's", "Master's"]


def test_scrum_master_is_not_a_degree():
    assert extract_education("Scrum master")["levels"] == []


def test_generic_degree_has_no_level():
    result = extract_education("Any degree")
    assert result["levels"] == []
    assert result["degree_mentioned"] is True


def test_no_degree_mentioned():
    result = extract_education("Python")
    assert result["levels"] == []
    assert result["degree_mentioned"] is False


def test_plain_word_be_is_not_a_degree():
    assert extract_education("You will be a team player")["levels"] == []


def test_diploma_is_detected():
    assert extract_education("Diploma in computer engineering")["levels"] == ["Diploma"]


def test_empty_text_has_no_education():
    assert extract_education("") == {"levels": [], "degree_mentioned": False}