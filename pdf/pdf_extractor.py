
from io import BytesIO
from pypdf import PdfReader


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract text from an in-memory PDF."""

    pdf_stream = BytesIO(pdf_bytes)
    reader = PdfReader(pdf_stream)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)
