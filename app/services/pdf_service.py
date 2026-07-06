from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.exceptions import CorruptPdfError

def pdf_summary(file_bytes: bytes):
    try:
        reader = PdfReader(BytesIO(file_bytes))
    except PdfReadError as exc:
        raise CorruptPdfError() from exc

    pages = len(reader.pages)

    text_chunks = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_chunks.append(page_text)

    full_text = "\n".join(text_chunks)

    preview = full_text[:25].replace("\n", " ").strip()
    if len(full_text) > 25:
        preview += "..."

    return {
        "pages": pages,
        "characters": len(full_text),
        "preview": preview,
    }