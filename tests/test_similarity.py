from ml.similarity import text_similarity


def test_identical_texts_are_100():
    assert text_similarity("python sql docker", "python sql docker") == 100


def test_no_shared_words_is_0():
    assert text_similarity("python sql", "baking bread") == 0


def test_empty_text_gives_none():
    assert text_similarity("", "python") is None
    assert text_similarity("python", "") is None


def test_only_common_words_gives_none():
    assert text_similarity("the and of", "the and of") is None


def test_similarity_is_symmetric():
    a, b = "python pandas machine learning", "python machine learning docker"
    assert text_similarity(a, b) == text_similarity(b, a)


def test_more_overlap_scores_higher():
    resume = "python pandas machine learning"
    close = "python pandas machine learning engineer"
    far = "baking bread cakes python"
    assert text_similarity(resume, close) > text_similarity(resume, far)


def test_capitals_do_not_matter():
    assert text_similarity("PYTHON SQL", "python sql") == 100