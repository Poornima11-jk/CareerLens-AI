import re
import unicodedata

BULLET_CHARS = "•●▪◦■□▶►"


def clean_text(text: str) -> str:
    """Tidy raw PDF text but keep line breaks and capital letters."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", text)
    for bullet in BULLET_CHARS:
        text = text.replace(bullet, " ")
    text = text.replace("\t", " ")
    text = re.sub(r" {2,}", " ", text)
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_for_matching(text: str) -> str:
    """Lowercase text with single spaces, keeping symbols like + # . / -"""
    text = clean_text(text).lower()
    text = re.sub(r"[^a-z0-9+#./\-\s]", " ", text)
    text = re.sub(r"\.+(?=\s|$)", " ", text)
    text = re.sub(r"(?<!\S)-+(?!\S)", " ", text)
    return " ".join(text.split())