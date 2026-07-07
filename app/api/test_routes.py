from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_returns_summary_for_valid_pdf():
    pdf_path = Path("sample/minimal-document.pdf")

    with pdf_path.open("rb") as f:
        response = client.post(
            "/upload",
            files={"file": (pdf_path.name, f, "application/pdf")},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == pdf_path.name
    assert body["page_count"] >= 1
    assert "preview" in body
    assert body["character_count"] >= 1


def test_upload_rejects_invalid_file_type():
    response = client.post(
        "/upload",
        files={"file": ("notes.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 415
    assert response.json()["detail"]["error_code"] == "unsupported_file_type"


def test_upload_rejects_empty_pdf():
    empty_pdf_bytes = b"%PDF-1.4\n%\x00\x00\x00\ninvalid pdf content"

    response = client.post(
        "/upload",
        files={"file": ("empty.pdf", empty_pdf_bytes, "application/pdf")},
    )

    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "corrupt_pdf"
