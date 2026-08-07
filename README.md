## Project

```
Insights Hub
```

## Features

- Upload PDFs
- Extract text
- Health endpoint
- Swagger documentation

## Prerequisites

- Python 3.10+ installed
- Git (optional)

## Quick start (local)

1. Create and activate a virtual environment

Windows (PowerShell):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```
python -m pip install -r requirements.txt
```

3. Configure environment

Create a `.env` file in the project root or set `DATABASE_URL` in your environment. Example `.env`:

```
DATABASE_URL=sqlite:///./dev.db
```

4. Run database migrations (Alembic)

Initialize / upgrade the database schema:

```
alembic upgrade head
```

Create a new migration after model changes:

```
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

5. Run the app

```
uvicorn app.main:app --reload
```

Open the API docs at: http://127.0.0.1:8000/docs

## How to use

- Upload PDF (POST): `/upload` — multipart form, field name `file`.
- List documents (GET): `/documents`
- Get document (GET): `/documents/{id}`
- Download stored file (GET): `/documents/{id}/download`

Example curl upload:

```
curl -F "file=@sample/minimal-document.pdf;type=application/pdf" http://127.0.0.1:8000/upload
```

Example download:

```
curl -O http://127.0.0.1:8000/documents/1/download
```

## Testing

Run unit and API tests with pytest:

```
python -m pytest -q
```

Tests use temporary storage and monkeypatching; they do not require a running server.

## Development tooling

- Lint: `ruff .`
- Format: `black .`

## Notes

- Storage: uploaded files are saved under the `storage/` directory by `StorageService`.
- Migrations: Alembic is configured in the `alembic/` folder — always generate and apply migrations when changing models.
- For large files prefer serving from disk (`FileResponse`) or streaming (`StreamingResponse`) to avoid loading entire files into memory.
