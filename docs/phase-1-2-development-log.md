# Phase 1/2 - FastAPI Upload API Development Log

## Project goal

Build a small FastAPI application that accepts PDF uploads, extracts text in memory, and returns a structured summary payload. Organize routes, services, schemas, and error handling in a beginner-friendly way that is easy to extend.

## Development iterations

### 1. Creating the first FastAPI app

- Built a minimal FastAPI application with a simple root endpoint.
- Learned the basic pattern for creating an app instance with FastAPI.
- Verified that the app could run locally with Uvicorn.

### 2. Introducing APIRouter

- Moved route definitions out of the main app file into an API router module.
- Learned how to include routers in the main FastAPI app.
- This made the project easier to organize as the endpoint count grew.

### 3. Creating the upload endpoint

- Added a POST endpoint for file upload.
- Used FastAPI’s UploadFile and File() to accept multipart/form-data.
- Learned that uploaded file content is read asynchronously with await file.read().

### 4. Processing PDF bytes in memory

- Used BytesIO and PdfReader to parse uploaded PDF bytes without saving files to disk.
- Kept the file-reading logic out of the route and placed it in a service module.
- Learned the pattern of passing bytes into a service and receiving structured data back.

### 5. Returning structured responses with Pydantic

- Defined a response model for successful uploads.
- Returned a Pydantic model from the route instead of a raw dictionary.
- Learned that Pydantic models are useful for validating and documenting API response shapes.

### 6. Adding meaningful error handling

- Added route-level checks for:
  - missing files
  - unsupported file types
  - invalid or corrupted PDFs
- Used HTTPException to return meaningful JSON errors with appropriate status codes.
- Added a global exception handler for unexpected server-side failures.

### 7. Organizing the project structure

- Introduced a clear separation between:
  - routes
  - services
  - schemas
  - core utilities
- This made the app easier to understand and extend as new features are added.

### 8. Improving the response payload

- Returned a compact summary payload containing:
  - filename
  - page_count
  - preview
  - character_count
- Learned how to keep the preview short and readable with simple string formatting.

## Current structure

- app/main.py
  - FastAPI app entry point
  - includes routers
  - registers the global exception handler
- app/api/routes.py
  - endpoint definitions for upload and health routes
- app/api/health.py
  - simple health endpoint router
- app/services/pdf_service.py
  - PDF extraction and summary logic
- app/schemas/upload.py
  - Pydantic schema for successful upload responses
- app/schemas/error.py
  - Pydantic schema for error responses
- app/core/exceptions.py
  - custom exception classes for upload-related errors
- app/core/exception_handlers.py
  - reusable handler functions for errors
- sample/
  - contains sample PDF files used for testing
- docs/
  - development log and project documentation

## How to run the app

From the project root, use:

```bash
uvicorn app.main:app --reload
```

Then open the Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

You can test the upload endpoint there.

## Key concepts learned

- APIRouter for modular route organization
- FastAPI UploadFile and multipart/form-data
- async endpoints for file I/O
- Pydantic models for response validation and documentation
- keeping business logic in services instead of routes
- returning structured JSON errors instead of letting Python crash
- separating API concerns from app setup

## Helpful syntax and patterns

- Use `@router.post(...)` to define route handlers in a router module.
- Use `UploadFile = File(...)` in the route to receive an uploaded file.
- Use `await file.read()` to read the upload bytes in memory.
- Use `response_model=...` to document and validate successful responses.
- Use `HTTPException` for clear and meaningful API errors.
- Use a service function to keep business logic out of the route layer.

## Notes for future improvements

- Add request/response examples to the API docs.
- Add tests for missing files, invalid types, corrupt PDFs, and successful uploads.
- Consider adding a database or persistent storage layer later.
- Explore dependency injection more deeply as the app grows.
