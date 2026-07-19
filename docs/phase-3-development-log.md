# Phase 3 - Data Persistence

## Project goal

Add a persistent storage layer so uploaded PDFs can be saved as database records instead of only being processed in memory. The goal was to introduce SQLAlchemy models, repository-style access, and a simple service boundary that keeps the API route focused on request handling.

## Structure built on this phase

Client
↓
API Router
↓
Service
↓
Repository
↓
SQLAlchemy
↓
PostgreSQL

## Development Iteration

### 1. Introducing SQLAlchemy models

- Added a `Document` ORM model mapped to a `documents` table.
- Defined key fields such as `id`, `filename`, `page_count`, and `uploaded_at`.
- Learned how SQLAlchemy declarative models are created with `Mapped` and `mapped_column`.

### 2. Creating the database layer

- Added a database module that creates the engine and session factory.
- Used a context-managed session pattern to ensure sessions are properly closed and rolled back on failure.
- Wired the project to use environment-based database configuration via `DATABASE_URL`.

### 3. Building a repository layer

- Created a `DocumentRepository` class to encapsulate common document persistence operations.
- Introduced methods such as `create`, `get_by_id`, `list`, and `delete`.
- Kept database write logic out of the route and moved it behind a repository abstraction.

### 4. Refactoring the upload flow around services

- Moved PDF parsing and summary generation into a service layer.
- Added logic to build a `Document` instance from the upload summary.
- Persisted the document through the repository after parsing the uploaded PDF.
- Kept the route responsible for validating the request and returning the API response.

### 5. Aligning the route with the new persistence model

- Updated the upload endpoint to create a `Document` object from the uploaded file metadata.
- Saved the document with the repository before returning the upload response.
- Learned that the route should not directly own session lifecycle logic when a service/repository abstraction is available.

### 6. Key architectural takeaway

- The upload route became slimmer and easier to read.
- Business logic was separated into distinct layers:
  - route: HTTP concerns
  - service: PDF processing and orchestration
  - repository: database persistence
  - model: ORM representation of the saved record

## Current structure

- app/api/routes.py
  - upload endpoint and request validation
- app/services/pdf_service.py
  - PDF summary extraction and document persistence orchestration
- app/repositories/document_repository.py
  - repository methods for document CRUD operations
- app/models/document.py
  - SQLAlchemy model for the documents table
- app/database/database.py
  - SQLAlchemy engine/session setup and context-managed session access

## Notes for future improvements

- Add stronger repository methods such as `get_all` or `get_by_filename`.
- Introduce database migrations once the schema grows.
- Add tests around database persistence and repository behavior.
- Consider moving the session lifecycle into a more formal dependency injection pattern.
