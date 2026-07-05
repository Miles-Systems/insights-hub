from pathlib import Path

from pypdf import PdfReader


def read_pdf(file_path):
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    reader = PdfReader(str(path))
    text = ""
    has_extractable_text = False

    for page_number, page in enumerate(reader.pages, start=1):
        pdf_text = page.extract_text()
        if pdf_text and pdf_text.strip():
            has_extractable_text = True
            text += f"Page {page_number}: {pdf_text}\n\n"
        else:
            text += f"Page {page_number}: [No text found on this page]\n\n"

    if not has_extractable_text:
        raise ValueError("This PDF does not contain any extractable text.")

    return text