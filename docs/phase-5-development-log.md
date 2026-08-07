# Phase 5 - Storage and Download

## Project goal

Add a concrete storage implementation for uploaded PDFs, wire persisted files into the API, and implement a robust download endpoint with tests.

## Structure built on this phase

Client
↓
API router
↓
Service
↓
StorageService (filesystem)
↓
File storage (`storage/uploads`)

## Development iteration

### 1. Storage service

- Introduced a `StorageService` responsible for saving upload bytes to disk, checking file existence, streaming reads, and resolving filesystem paths.
- Files are stored under a `storage` directory (subfolders created per-subdirectory), and `save()` returns a lightweight `StoredFile` metadata object.

### 2. Persisting uploaded files

- Updated upload flow to persist the uploaded file to disk via `StorageService.save(...)` during the upload processing path.
- The saved file's `storage_path`, `stored_filename` and `file_size` are returned in the upload response so clients can reference the stored artifact.

### 3. Download endpoint

- Implemented the `GET /documents/{document_id}/download` endpoint to serve persisted files.
- Endpoint flow:
  - Lookup document via service/repository.
  - Check existence with `StorageService.exists(storage_path)`.
  - Stream or read file bytes via `StorageService.read(...)` and serve using `FileResponse` (current implementation writes to a temporary file before returning `FileResponse`).
  - Log the download preparation step and schedule temporary cleanup when applicable.

### 4. Tests and test helpers

- Added `tests/api/test_storage_service.py` to validate `save()`, `exists()`, `read()` (chunked read), and `get_path()` behavior.
- Added `tests/api/test_download.py` with three cases:
  - Successful download returns 200 and correct bytes.
  - Missing document returns 404 with `document_not_found` error.
  - Document exists but file missing returns 404 with `file_not_found` error.
- Tests use small test fixtures and monkeypatching to avoid touching production storage and to simulate document/service behavior.

## Current structure (high level)

- `app/services/storage_service.py` — storage helpers: `save`, `exists`, `read`, `get_path`
- `app/api/routes.py` — download endpoint wiring, logging, and temporary-file handling for `FileResponse`
- `tests/api/test_storage_service.py` — unit tests for `StorageService`
- `tests/api/test_download.py` — endpoint-level tests that monkeypatch services

## Notes and considerations

- Temporary-file approach: current download handler writes bytes to a temp file for `FileResponse`. For large files prefer returning `FileResponse` with the real filesystem path (or using `StreamingResponse`) to avoid double I/O and extra disk usage.
- Tests intentionally monkeypatch `StorageService` and `DocumentService` to keep test scope small and deterministic.
- Ensure deployments run DB migrations (Alembic) and that any new fields related to storage metadata are included in migrations.

## Next steps

- Replace temporary-file download path with direct `FileResponse(path=storage_path)` where possible, or convert to `StreamingResponse` backed by `StorageService.read()` for remote/streamed storage.
- Add integration tests that exercise the full upload → persist → download cycle.
- Document storage layout and add short `README.md` snippet describing how to run local tests that touch the storage layer.
