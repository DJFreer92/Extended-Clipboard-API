# Extended-Clipboard-API

## Overview

Small FastAPI service and utilities for persisting clipboard entries to a local SQLite database and fetching recent clips. The project favors a simple, layered design: endpoints (HTTP) → services (business logic) → DB helpers/queries (data access) → schema (DDL).

## Features

- Persist new clipboard entries to `clipboard.db`
- Fetch the N most recent clipboard entries
- FastAPI app with clean separation of concerns
- Database schema and queries are stored as SQL files in the repo

## Tech stack

- Python 3.13
- FastAPI, Uvicorn, Pydantic
- SQLite (via Python stdlib)
- SQLAlchemy listed in requirements but not used by current modules

## Repository structure

```text
LICENSE                         # Project license
README.md                       # This file
requirements.txt                # Python dependencies
app/
  api/
    __init__.py
    main.py                     # FastAPI app entry (includes routers)
    clipboard/
      clipboard_endpoints.py    # HTTP routes for clipboard
  core/
    constants.py                # Paths and constants
  db/
    __init__.py
    db.py                       # DB helpers (init_db, execute_query)
    clipboard.db                # SQLite database (created on first init)
    queries/                    # Reusable SQL query files
      add_clip.sql
      get_n_clips.sql
    schema/                     # DDL: tables, indexes, triggers, views
      tables/
        clips.sql
      triggers/
        delete_old_if_duplicate.sql
      indexes/
      views/
  models/
    clipboard/
      clipboard_models.py       # Pydantic models (request/response)
  services/
    __init__.py
    clipboard/
      clipboard_service.py      # Business logic for clipboard
scripts/
  create_db.py                  # Initializes DB schema (runs init_db)
  run_api.py                    # Helper script to run the API
  run_poller.py                 # Optional: example poller/ingestion script
tests/
  test_query.py                 # Simple manual test script for queries
.github/
  copilot-instructions.md       # Copilot repository instructions
  instructions/                 # Language-specific Copilot instruction files
```

## Getting started

Prerequisites:

- Python 3.13 installed

Setup:

```bash
# From repo root
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Initialize the database schema:

```bash
python scripts/create_db.py
```

## Run the API

You can run the server via Uvicorn or the helper script.

```bash
# Option A: Uvicorn directly
uvicorn app.api.main:app --reload

# Option B: Helper script
python scripts/run_api.py
```

Visit the interactive docs:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## API endpoints

- GET `/clipboard/get_recent_clips?n=10`
  - Query params: `n` (int, default 10, min 1)
  - Response body (example):

    ```json
    {
      "clips": [ { "content": "..." } ]
    }
    ```

  - Example:

    ```bash
    curl "http://127.0.0.1:8000/clipboard/get_recent_clips?n=5"
    ```

- POST `/clipboard/add_clip`
  - Adds a new clipboard entry.
  - Request body (application/json):

    ```json
    { "content": "Hello World" }
    ```

  - Example:

    ```bash
    curl -X POST \
      -H "Content-Type: application/json" \
      -d '{"content":"Hello World"}' \
      "http://127.0.0.1:8000/clipboard/add_clip"
    ```

## Database

- File: `app/db/clipboard.db` (created on first init)
- Schema: SQL files under `app/db/schema/**` (tables, indexes, triggers, views)
- Queries: Reusable SQL under `app/db/queries/**`; executed via helpers in `app/db/db.py`

## Development notes

- Keep logic layered: Endpoints → Services → DB helpers/queries → Schema.
- Add new queries as `.sql` files in `app/db/queries/` and execute via the DB helper in `app/db/db.py`.
- If you change behavior, add/update tests under `tests/`.

Manual query sanity check:

```bash
python tests/test_query.py
```

## Testing

Unit tests are written with pytest and cover endpoints, services, and the database (queries + triggers).

Prerequisites:

- Activate the virtual environment and install dependencies.
- Install pytest (dev dependency):

```bash
pip install pytest
```

Run all tests from the repository root:

```bash
pytest -q
```

Run only service tests:

```bash
pytest tests/service_tests -q
```

Run only endpoint tests:

```bash
pytest tests/endpoint_tests -q
```

Run only database (queries + triggers) tests:

```bash
pytest tests/db_tests -q
```

Notes:

- Tests rely on `tests/conftest.py` to bootstrap imports; run pytest from the repo root so modules import cleanly.
- Service tests mock DB access (`execute_query`), and endpoint tests mock service calls, so no real database or network is used.
- Database tests run against a real, isolated SQLite database file created under a temporary directory. They patch the DB path and call `init_db()` so actual schema and triggers are applied. The temporary DB is deleted automatically after tests, and `app/db/clipboard.db` is never touched.

## Troubleshooting

- “Database already exists. Skipping init.” means the schema init was previously run; delete `app/db/clipboard.db` if you want a fresh database.
- If imports fail when running scripts, ensure you’re executing from the repo root with the virtual environment activated.

## License

This project is licensed under the terms of the LICENSE file included in this repository.
