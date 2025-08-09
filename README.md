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
clipboard.db               # SQLite database (created on first init)
requirements.txt           # Python dependencies
app/
  main.py                  # FastAPI app entry
  endpoints/               # HTTP routes (routers)
  services/                # Business logic
  models/                  # Pydantic models (request/response)
  core/
    db.py                  # DB helpers (init_db, execute_query)
    db_constants.py        # Paths and constants
    schema/                # DDL: tables, indexes, triggers, views
queries/                   # Reusable SQL query files
scripts/
  create_db.py             # Initializes DB schema (runs init_db)
tests/
  test_query.py            # Simple manual test script for queries
.github/
  copilot-instructions.md  # Copilot repository instructions
  instructions/            # Language-specific Copilot instruction files
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

```bash
uvicorn app.main:app --reload
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

- POST `/clipboard/add_clip?content=...`
  - Adds a new clipboard entry.
  - For simple usage, `content` is passed as a query parameter.
  - Example:

    ```bash
    curl -X POST "http://127.0.0.1:8000/clipboard/add_clip?content=Hello%20World"
    ```

## Database

- File: `clipboard.db` at repo root (created on first init)
- Schema: SQL files under `app/core/schema/**` (tables, indexes, triggers, views)
- Queries: Reusable SQL under `queries/`; executed via `app/core/db.execute_query()`

## Development notes

- Keep logic layered: Endpoints → Services → DB helpers/queries → Schema.
- Add new queries as `.sql` files in `queries/` and execute via the DB helper.
- If you change behavior, add/update tests under `tests/`.

Manual query sanity check:

```bash
python tests/test_query.py
```

## Troubleshooting

- “Database already exists. Skipping init.” means the schema init was previously run; delete `clipboard.db` if you want a fresh database.
- If imports fail when running scripts, ensure you’re executing from the repo root with the virtual environment activated.

## License

This project is licensed under the terms of the LICENSE file included in this repository.
