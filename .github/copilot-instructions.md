# Extended-Clipboard-API — Copilot repository instructions

These instructions provide project-level context and conventions. Language-specific rules live in `.github/instructions/*.instructions.md`.

## Project overview
- Purpose: Provide a small REST API and utilities to persist clipboard entries and fetch recent clips.
- API framework: FastAPI app in `app/main.py`; routes under `app/endpoints/**`; services in `app/services/**`; data models in `app/models/**`.
- Data: SQLite database file `clipboard.db` in the repo root. Schema and DDL live under `app/core/schema/**`. Reusable SQL queries live under `queries/`.
- Data access: `app/core/db.py` offers helpers (e.g., `init_db`, `execute_query`) that load SQL from files and execute with parameters.
- Entrypoints: `app/main.py` (FastAPI). `scripts/create_db.py` initializes the DB schema.
- Environment: Python 3.13. Key deps: FastAPI, Uvicorn, Pydantic, SQLite (via stdlib), SQLAlchemy present but not used by current modules.

## Architectural conventions (non language-specific)
- Keep responsibilities separated:
  - Endpoints (HTTP concerns) → Services (business logic) → DB helpers/queries (data access) → Schema (DDL).
- Prefer reading SQL from files in `queries/` instead of embedding SQL strings in code. Add new query files when adding new operations.
- Store schema changes as SQL files in `app/core/schema/**` (tables, indexes, triggers, views). Avoid DDL in application code.
- Follow existing folder layout; avoid introducing new frameworks or patterns without need.
- When implementing a feature, update all impacted layers minimally rather than concentrating logic in one place.
- Add or update tests in `tests/` when changing behavior.

## How Copilot should help
- Align suggestions with the existing structure and files.
- Route data access through the DB helper layer that reads SQL from files.
- Reference existing files when possible instead of generating large, speculative code.
- If multiple files need changes (endpoint, service, query, schema), propose focused edits across layers.

For language-specific style and best practices, see:
- `.github/instructions/python.instructions.md`
- `.github/instructions/sqlite.instructions.md`
