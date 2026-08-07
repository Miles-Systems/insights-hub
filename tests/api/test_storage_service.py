import io
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.services.storage_service import StorageService


@pytest.fixture
def sample_upload_file():
    file_path = Path("sample/minimal-document.pdf")
    file_bytes = file_path.read_bytes()
    return SimpleNamespace(
        file=io.BytesIO(file_bytes),
        filename=file_path.name,
        content_type="application/pdf",
    )


@pytest.fixture
def storage_service(monkeypatch, tmp_path):
    monkeypatch.setattr("app.services.storage_service.BASE_STORAGE_PATH", tmp_path)
    return StorageService()


def test_save_writes_file_and_returns_stored_file_metadata(
    storage_service, sample_upload_file, tmp_path
):
    stored_file = storage_service.save(sample_upload_file, subdirectory="uploads")
    expected_path = tmp_path / "uploads" / stored_file.stored_filename

    assert expected_path.exists()
    assert stored_file.storage_path == f"uploads/{stored_file.stored_filename}"
    assert stored_file.original_filename == sample_upload_file.filename
    assert stored_file.file_size == expected_path.stat().st_size
    assert stored_file.mime_type == "application/pdf"


def test_exists_returns_true_for_saved_file_and_false_for_missing(
    storage_service, sample_upload_file
):
    stored_file = storage_service.save(sample_upload_file, subdirectory="uploads")

    assert storage_service.exists(stored_file.storage_path)
    assert not storage_service.exists("uploads/missing-file.pdf")


# def test_read_returns_chunked_file_content(storage_service, sample_upload_file):
#     original_bytes = Path("sample/minimal-document.pdf").read_bytes()
#     stored_file = storage_service.save(sample_upload_file, subdirectory="uploads")

#     chunks = list(storage_service.read(stored_file.storage_path, chunk_size=32))
#     assert chunks
#     assert b"".join(chunks) == original_bytes


def test_get_path_returns_filesystem_path(
    storage_service, sample_upload_file, tmp_path
):
    stored_file = storage_service.save(sample_upload_file, subdirectory="uploads")
    expected_path = tmp_path / stored_file.storage_path

    assert storage_service.get_path(stored_file.storage_path) == expected_path
