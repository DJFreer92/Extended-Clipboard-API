---
applyTo: "**/*.sql"
description: "SQLite (SQL) best practices and code style for this repo (applies to .sql files)."
---

# SQLite guidelines for Extended-Clipboard-API

Use these rules for SQL files in this repository. Keep language-agnostic guidance in the global instructions.

## General
- Target SQLite syntax/features only; avoid vendor-specific extensions.
- Keep each file focused: schema DDL under `app/core/schema/**` (tables, indexes, triggers, views); data operations under `queries/`.
- Name files by intent, e.g., `add_clip.sql`, `get_n_clips.sql`. Prefer one statement per file for clarity unless a script is required.

## Style
- Uppercase SQL keywords (`SELECT`, `INSERT`, `UPDATE`, `WHERE`, `JOIN`).
- Use snake_case for identifiers. Keep table and column names concise and descriptive.
- Prefer explicit column lists in `INSERT` and `SELECT` statements; avoid `SELECT *` in reusable queries.
- End files without trailing semicolons when the file contains a single statement executed via `cursor.execute`.

## Parameters
- Always use parameter placeholders (`?`) and bind values from Python. Do not inline values.
- Keep parameter order stable and document expected parameters at the top of the file using comments.

## Constraints & indexes
- Define primary keys and necessary unique constraints in table DDL under `schema/tables/`.
- Create supporting indexes in `schema/indexes/` with clear names (e.g., `idx_clips_created_at`).

## Triggers & views
- Keep triggers simple and idempotent; prefer clear names and include a brief comment describing the purpose.
- Views should expose only the columns needed by consumers and avoid complex logic that belongs in application code.

## Data integrity
- Use `CHECK` constraints for basic validation where appropriate.
- When deduplication is required, prefer `INSERT OR IGNORE` with unique constraints, or explicit de-duplication queries.

## Comments
- At the top of each query file, include a short comment block documenting:
  - Purpose
  - Parameters (order and meaning)
  - Expected result shape
