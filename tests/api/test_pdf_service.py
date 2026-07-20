from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.document import Document
from app.services.pdf_service import PDFService

client = TestClient(app)


@pytest.fixture
def sample_pdf_bytes():
    pdf_path = Path("sample/minimal-document.pdf")
    return pdf_path.read_bytes()


def test_pdf_summary_returns_expected_keys(sample_pdf_bytes):
    service = PDFService()
    summary = service.pdf_summary(sample_pdf_bytes, filename="minimal-document.pdf")

    assert summary["filename"] == "minimal-document.pdf"
    assert summary["pages"] >= 1
    assert summary["characters"] >= 1
    assert "preview" in summary


def test_save_document_persists_a_document(sample_pdf_bytes):
    service = PDFService()
    summary = service.pdf_summary(sample_pdf_bytes, filename="minimal-document.pdf")
    document = service.save_document(summary)

    assert isinstance(document, Document)
    assert document.filename == "minimal-document.pdf"
    assert document.page_count >= 1
    assert document.id is not None


def test_get_documents_returns_document_responses():
    service = PDFService()
    documents = service.get_documents()

    assert isinstance(documents, list)
    assert all(hasattr(item, "id") for item in documents)
    assert all(hasattr(item, "filename") for item in documents)


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
