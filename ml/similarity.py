from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ml.preprocessing import normalize_for_matching


def text_similarity(resume_text: str, job_text: str):
    resume = normalize_for_matching(resume_text)
    job = normalize_for_matching(job_text)
    if not resume or not job:
        return None

    try:
        matrix = TfidfVectorizer(stop_words="english").fit_transform([resume, job])
    except ValueError:
        return None  # nothing left after removing common words

    score = cosine_similarity(matrix[0], matrix[1])[0][0]
    return round(float(score) * 100)