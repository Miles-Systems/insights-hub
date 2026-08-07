# Phase 4 - API responses, retrieval, and persistence

## Project goal

Standardize API responses for documents, add retrieval endpoints (collection and single-item), improve validation and error handling, and persist an extracted `character_count` value via database migrations.

## Structure built on this phase

Client
↓
API router
↓
Service
↓
Repository
↓
SQLAlchemy + Alembic
↓
PostgreSQL

## Development iteration

### 1. Document response schema

- Introduced a dedicated response schema for documents to normalize API output and make client contracts explicit.
- Moved presentation concerns out of domain models and into `schemas` so services and repositories return stable shapes.

### 2. GET endpoints for documents

- Implemented a collection `GET /documents` endpoint to list persisted documents.
- Implemented a `GET /documents/{id}` endpoint to retrieve a single document by id.
- Routed retrieval logic through the service and repository layers to keep routes thin and focused on HTTP concerns.

### 3. Validation and error handling

- Reordered validation and 404 checks so missing resources return 404 before attempting schema validation where applicable.
- Simplified model validation and corrected import paths; minor refactors improved readability and reduced accidental coupling between layers.

### 4. Migrations and schema evolution

- Configured Alembic for database migrations and added the scaffold to manage schema changes going forward.
- Added a migration to evolve the `documents` table when new fields were needed.

### 5. Persisting `character_count`

- Added a `character_count` field to the `Document` model and updated upload/processing flows to calculate and store the count when persisting a document.
- Ensured the repository and service layers persist the new field and that response schemas expose it where relevant.

## Current structure (high level)

- `app/api/routes.py` — upload and retrieval endpoints; routing and request/response wiring
- `app/schemas/document.py` — response schema for documents (separates presentation from persistence)
- `app/services/pdf_service.py` — PDF parsing, summary extraction, and orchestration for persistence
- `app/repositories/document_repository.py` — persistence operations including create, list, and get_by_id
- `app/models/document.py` — SQLAlchemy model updated with `character_count`
- `alembic/` and migration scripts — Alembic configuration and migrations to evolve DB schema

## Notes and considerations

- Backwards compatibility: the new response schema may alter the JSON shape returned to clients; document any contract changes for API consumers.
- Migrations: run Alembic migrations when provisioning or refreshing databases to ensure schema and code stay in sync.

## Next steps

- Add tests to cover `character_count` calculation and persistence and to exercise the newly added GET endpoints.
- Update the README or deployment notes with concise Alembic commands for local development and deployment.
- Consider adding feature flags or versioned API responses if a non-breaking migration path is needed for API consumers.
