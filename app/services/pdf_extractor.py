from io import BytesIO

from pypdf import PdfReader

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


class ResumeError(Exception):
    """A problem with the uploaded resume, with a user-friendly message."""


def extract_text_from_pdf(file_bytes: bytes) -> str:
    if not file_bytes:
        raise ResumeError("The file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ResumeError("The file is too large. Maximum size is 5 MB.")

    if not file_bytes.startswith(b"%PDF"):
        raise ResumeError("This does not look like a valid PDF file.")

    try:
        reader = PdfReader(BytesIO(file_bytes))
        pages = [page.extract_text() or "" for page in reader.pages]
    except Exception:
        raise ResumeError(
            "Could not read this PDF. It may be damaged or password-protected."
        )

    text = "\n".join(pages).strip()
    if not text:
        raise ResumeError(
            "No text detected. This may be a scanned image. "
            "Please upload a PDF with selectable text."
        )

    return text