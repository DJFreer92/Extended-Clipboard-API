# Extended Clipboard API

A small FastAPI service for persisting clipboard entries in an encrypted SQLite (SQLCipher) database and retrieving them with flexible filters.

Desktop app (UI) that uses this API:

- Extended Clipboard Desktop App: <https://github.com/DJFreer92/Extended-Clipboard-Desktop-App>

## Why this project

- Local-first clipboard history with tagging, favorites, and source app tracking
- Clean layers: Endpoints (HTTP) → Services (logic) → Queries (SQL files) → Schema (DDL)
- Encrypted by default via SQLCipher, accessed through a Node.js runner

## Tech stack

- Python 3.13, FastAPI, Uvicorn, Pydantic
- SQLite + SQLCipher (via a Node runner using better-sqlite3-multiple-ciphers)
- Tests with pytest

## Repository structure

```text
LICENSE
README.md
requirements.txt
package.json
app/
  api/
    __init__.py
    main.py                      # FastAPI app entry (includes routers)
    clipboard/
      clipboard_endpoints.py     # All /clipboard endpoints
  core/
    constants.py                 # Paths and query file constants
  db/
    __init__.py
    db.py                        # Node-backed DB helpers (init_db, execute_query)
    queries/                     # Reusable SQL files (1 statement per file)
    schema/                      # DDL organized by type
      tables/
      indexes/
      triggers/
      views/
  models/
    clipboard/                   # Pydantic models & filters
  services/
    clipboard/                   # Business logic
scripts/
  create_db.py                   # Initialize schema (via Node runner)
  seed_db.py                     # Seed sample data (timestamps, tags, favorites)
  run_api.py                     # Start FastAPI server
  run_poller.py                  # Example ingestion/poller script
tests/
  endpoint_tests/
  service_tests/
  db_tests/
.github/
  copilot-instructions.md
  instructions/
```

## Prerequisites

- Python 3.13
- Node.js (LTS) + npm
- An encryption key exported as an environment variable (required):

```bash
export CLIPBOARD_DB_KEY="change-me-strong-passphrase"
```

Install Python deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install Node deps and the SQLCipher-capable driver:

```bash
npm install
npm install better-sqlite3-multiple-ciphers
```

## Initialize or seed the database

- Initialize schema only:

```bash
python scripts/create_db.py
```

- Seed with sample data (100 clips over ~2 years, random tags/favorites):

```bash
python scripts/seed_db.py
```

Notes:

- The database lives at `app/db/clipboard.db`.
- All SQL is executed through `scripts/db_runner.mjs`; each query file must contain a single statement.

## Run the API

Start the server (two options):

```bash
# Option A: Uvicorn directly
uvicorn app.api.main:app --reload

# Option B: Helper script
python scripts/run_api.py
```

## Endpoints overview

Base path: `/clipboard`

Clips:

- GET `/get_recent_clips?n=10` → { "clips": Clip[] }
- GET `/get_all_clips` → { "clips": Clip[] }
- GET `/get_all_clips_after_id?before_id=<int>` → { "clips": Clip[] }
- GET `/get_n_clips_before_id?n=<int>&before_id=<int>` → { "clips": Clip[] }
- GET `/get_num_clips` → number
- POST `/add_clip` (body: { content: string }, optional query: from_app_name)
- POST `/delete_clip?id=<int>`
- POST `/delete_all_clips`

Filtering (all return { "clips": Clip[] }):

- GET `/filter_all_clips`
- GET `/filter_n_clips`
- GET `/filter_all_clips_after_id`
- GET `/filter_n_clips_before_id`
- GET `/get_num_filtered_clips` → number

Common query params for filters:

- `search`: string (keywords split by space, comma, semicolon, pipe, tab, newline)
- `time_frame`: one of `past_24_hours | past_week | past_month | past_3_months | past_year` (empty = all time)
- `selected_tags`: repeated query param or array syntax
- `selected_apps`: repeated query param or array syntax
- `favorites_only`: boolean

Tags:

- POST `/add_clip_tag?clip_id=<int>&tag_name=<string>`
- POST `/remove_clip_tag?clip_id=<int>&tag_id=<int>`
- GET `/get_all_tags` → { "tags": { id, name }[] }
- GET `/get_num_clips_per_tag?tag_id=<int>` → number

Favorites:

- POST `/add_favorite?clip_id=<int>`
- POST `/remove_favorite?clip_id=<int>`
- GET `/get_all_favorites` → { "clip_ids": number[] }
- GET `/get_num_favorites` → number

Apps:

- GET `/get_all_from_apps` → string[] (distinct non-null `FromAppName` values)

Clip model shape (response):

- `{ id: number, content: string, from_app_name: string | null, tags: string[], timestamp: string, is_favorite: boolean }`

## Testing

```bash
pip install pytest
pytest -q
```

Tips:

- Run tests from the repo root so imports resolve.
- DB tests require `better-sqlite3-multiple-ciphers` and `CLIPBOARD_DB_KEY` to be set.

## Troubleshooting

- Error: `Missing database key. Set the CLIPBOARD_DB_KEY ...` → Export `CLIPBOARD_DB_KEY` before running.
- Error: `SQLCipher not available...` → Ensure `better-sqlite3-multiple-ciphers` is installed (and Node is available).
- Query errors like "more than one statement" → Ensure each `.sql` file in `app/db/queries/` contains exactly one statement.

## License

See [LICENSE](./LICENSE).
