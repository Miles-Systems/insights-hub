from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_successful_download(monkeypatch, tmp_path):
    # Create a temporary file to act as stored PDF
    uploads_dir = tmp_path / "uploads"
    uploads_dir.mkdir(parents=True)
    file_path = uploads_dir / "test.pdf"
    file_bytes = b"PDF-TEST-BYTES"
    file_path.write_bytes(file_bytes)

    # Patch DocumentService.get_document to return a document-like object
    def _get_document(self, document_id):
        return SimpleNamespace(
            id=document_id,
            storage_path=str(file_path.relative_to(tmp_path)),
            mime_type="application/pdf",
            filename=file_path.name,
        )

    monkeypatch.setattr(
        "app.services.document_service.DocumentService.get_document", _get_document
    )

    # Patch StorageService.exists and get_path to point to our temp file
    monkeypatch.setattr(
        "app.services.storage_service.StorageService.exists", lambda self, sp: True
    )
    monkeypatch.setattr(
        "app.services.storage_service.StorageService.get_path",
        lambda self, sp: file_path,
    )

    response = client.get("/documents/1/download")
    assert response.status_code == 200
    assert response.content == file_bytes


def test_document_not_found_returns_404(monkeypatch):
    monkeypatch.setattr(
        "app.services.document_service.DocumentService.get_document",
        lambda self, document_id: None,
    )

    response = client.get("/documents/999/download")
    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "document_not_found"


def test_file_missing_returns_404(monkeypatch):
    # Document exists
    monkeypatch.setattr(
        "app.services.document_service.DocumentService.get_document",
        lambda self, document_id: SimpleNamespace(
            id=document_id,
            storage_path="uploads/missing.pdf",
            mime_type=None,
            filename="missing.pdf",
        ),
    )

    # File does not exist
    monkeypatch.setattr(
        "app.services.storage_service.StorageService.exists", lambda self, sp: False
    )

    response = client.get("/documents/2/download")
    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "file_not_found"
