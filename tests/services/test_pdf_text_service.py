from pathlib import Path

import fitz
import pytest

from app.core.exceptions import PDFExtractionError
from app.services.pdf_text_service import PDFTextService


class DummyStorageService:
    def __init__(self, path: Path):
        self.path = path

    def exists(self, storage_path: str) -> bool:
        return self.path.exists()

    def get_path(self, storage_path: str) -> Path:
        return self.path


def write_test_pdf(path: Path, pages: list[str]) -> None:
    doc = fitz.open()
    for page_text in pages:
        doc.new_page()
        if page_text:
            page = doc[-1]
            page.insert_text((72, 72), page_text)
    doc.save(str(path))
    doc.close()


def test_valid_pdf_returns_correct_number_of_pages_and_text(tmp_path: Path):
    pdf_path = tmp_path / "valid.pdf"
    page_texts = ["First page content", "Second page content"]
    write_test_pdf(pdf_path, page_texts)

    service = PDFTextService(DummyStorageService(pdf_path))
    extracted_pages = service.extract_text("valid.pdf")

    assert len(extracted_pages) == 2
    assert [page.page_number for page in extracted_pages] == [1, 2]
    assert [page.text.strip() for page in extracted_pages] == page_texts


def test_empty_page_returns_empty_text(tmp_path: Path):
    pdf_path = tmp_path / "empty_page.pdf"
    write_test_pdf(pdf_path, [""])

    service = PDFTextService(DummyStorageService(pdf_path))
    extracted_pages = service.extract_text("empty_page.pdf")

    assert len(extracted_pages) == 1
    assert extracted_pages[0].page_number == 1
    assert extracted_pages[0].text == ""


def test_missing_file_raises_file_not_found(tmp_path: Path):
    missing_path = tmp_path / "does-not-exist.pdf"
    service = PDFTextService(DummyStorageService(missing_path))

    with pytest.raises(FileNotFoundError):
        service.extract_text("does-not-exist.pdf")


def test_empty_pdf_raises_pdf_extraction_error():
    invalid_path = Path("sample/corrupted.pdf")

    service = PDFTextService(DummyStorageService(invalid_path))

    with pytest.raises(PDFExtractionError):
        service.extract_text("corrupted.pdf")


def test_corrupt_pdf_raises_pdf_extraction_error(tmp_path: Path):
    invalid_path = tmp_path / "placeholder-corrupted.pdf"
    invalid_path.write_bytes(b"%PDF-1.5\n%%EOF\nnot a real pdf")

    service = PDFTextService(DummyStorageService(invalid_path))

    with pytest.raises(PDFExtractionError):
        service.extract_text("corrupted.pdf")
