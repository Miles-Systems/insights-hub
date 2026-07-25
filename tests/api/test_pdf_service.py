import io
from pathlib import Path

from fastapi import UploadFile
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.document import Document, PDFSummary
from app.services.pdf_service import PDFService
from app.services.storage_service import StorageService

client = TestClient(app)


@pytest.fixture
def sample_upload_file():
    """Wraps PDF bytes into a proper FastAPI UploadFile object."""
    file_path = Path("sample/minimal-document.pdf")
    file_bytes = file_path.read_bytes()

    return UploadFile(
        file=io.BytesIO(file_bytes),
        filename=file_path.name,
    )


def test_pdf_summary_returns_expected_keys(sample_upload_file):
    service = PDFService()

    raw_bytes = sample_upload_file.file.read()
    summary = service.pdf_summary(raw_bytes, filename="minimal-document.pdf")

    assert isinstance(summary, PDFSummary)
    assert summary.filename == "minimal-document.pdf"
    assert summary.pages >= 1
    assert summary.characters >= 1
    assert summary.preview is not None


def test_save_document_persists_a_document(sample_upload_file):
    pdf_service = PDFService()
    upload_service = StorageService()

    raw_bytes = sample_upload_file.file.read()

    sample_upload_file.file.seek(0)

    uploaded_document = upload_service.save(sample_upload_file, subdirectory="uploads")

    summary = pdf_service.pdf_summary(raw_bytes, filename="minimal-document.pdf")
    document = pdf_service.save_document(summary, uploaded_document)

    assert isinstance(document, Document)
    assert document.filename == "minimal-document.pdf"
    assert document.page_count >= 1
    assert document.character_count is None or document.character_count >= 0
    assert document.id is not None


def test_get_documents_returns_document_responses():
    service = PDFService()
    documents = service.get_documents()

    assert isinstance(documents, list)
    assert all(hasattr(item, "id") for item in documents)
    assert all(hasattr(item, "filename") for item in documents)
    assert all(hasattr(item, "page_count") for item in documents)
    assert all(hasattr(item, "character_count") for item in documents)


def test_get_document_returns_document_response():
    service = PDFService()
    document = service.get_document(2)

    assert isinstance(document, Document)
    assert document.page_count >= 1
    assert document.character_count is None or document.character_count >= 0
    assert document.id is not None


def test_get_document_returns_none_for_missing_id():
    service = PDFService()
    document = service.get_document(999999)

    assert document is None


def test_documents_endpoint_returns_list_response():
    response = client.get("/documents")

    assert response.status_code == 200
    body = response.json()
    assert "documents" in body
    assert isinstance(body["documents"], list)


def test_document_detail_endpoint_returns_404_for_missing_id():
    response = client.get("/documents/999999")

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "document_not_found"
