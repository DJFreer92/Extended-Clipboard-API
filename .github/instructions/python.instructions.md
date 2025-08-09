---
applyTo: "**/*.py"
description: "Python code style and best practices for this repo (applies to .py files)."
---

# Python guidelines for Extended-Clipboard-API

Follow these language-specific rules for Python files. Keep project-agnostic guidance in the global instructions.

## Style and typing
- Target Python 3.13 syntax where appropriate, but keep compatibility with current code patterns.
- Use type hints on public functions, method signatures, and return values; prefer `list[str]` over `List[str]`.
- Keep functions small and single-purpose. Extract helpers when they reduce complexity or duplication.
- Prefer explicit imports over wildcard imports. Avoid `from x import *` in new code.
- Use f-strings for string formatting.
- Keep line length around 100–120 characters unless readability suffers.

## FastAPI
- Keep route definitions minimal; delegate all logic to service functions under `app/services/**`.
- Validate inputs using Pydantic models when payloads are non-trivial. Use simple query/path parameters for primitives.
- Return Pydantic models (from `app/models/**`) for responses when structured data is returned.

## Database access
- Do not embed raw SQL in Python code. Read queries from files in the `queries/` folder and execute via `app/core/db.execute_query`.
- Handle parameters safely using SQLite parameter substitution (pass tuples/dicts to `execute_query`). Never use string interpolation for SQL.
- If a new query is needed, create a `.sql` file in `queries/`, reference it from `app/core/db_constants.py` as a path, and call it via the DB helper.

## Errors and edge cases
- Check file existence and raise clear exceptions (`FileNotFoundError`, `ValueError`) when inputs are invalid.
- Validate external inputs at the boundary (endpoints) and keep internal functions assuming validated data when possible.

## Testing
- Add or update tests in `tests/` for new behavior. Keep tests small and focused; avoid side effects.

## Docs and structure
- Place new modules following the established layout: endpoints → services → models → core/db → queries/schema.
- Update README and instructions when adding significant capabilities or conventions.
