from io import BytesIO

import pytest
from pypdf import PdfWriter

from app.services.pdf_extractor import (
    MAX_FILE_SIZE_BYTES,
    ResumeError,
    extract_text_from_pdf,
)


def make_blank_pdf() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    buffer = BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_empty_file_is_rejected():
    with pytest.raises(ResumeError, match="empty"):
        extract_text_from_pdf(b"")


def test_non_pdf_file_is_rejected():
    with pytest.raises(ResumeError, match="valid PDF"):
        extract_text_from_pdf(b"This is just plain text, not a PDF.")


def test_too_large_file_is_rejected():
    big_file = b"%PDF" + b"0" * MAX_FILE_SIZE_BYTES
    with pytest.raises(ResumeError, match="too large"):
        extract_text_from_pdf(big_file)


def test_pdf_without_text_is_rejected():
    with pytest.raises(ResumeError, match="No text detected"):
        extract_text_from_pdf(make_blank_pdf())