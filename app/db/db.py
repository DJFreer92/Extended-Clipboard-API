"""Database helpers that execute SQL via a Node.js runner using SQLCipher.

This switches from Python's sqlite3 to an encrypted DB powered by
better-sqlcipher3. Python invokes a small Node script to run queries.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Callable

from ..core.constants import *
try:
    # Load environment variables from .env if present
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=BASE_DIR / ".env")
except Exception:
    # If python-dotenv isn't installed, continue; env vars may already be set
    pass

# Path to the Node runner
NODE_DB_RUNNER: Path = BASE_DIR / "scripts" / "db_runner.mjs"

# Env var for the SQLCipher key
DB_KEY_ENV: str = "CLIPBOARD_DB_KEY"


def _ensure_node_runner() -> None:
    if not NODE_DB_RUNNER.exists():
        raise FileNotFoundError(
            f"Node DB runner not found at {NODE_DB_RUNNER}. Create scripts/db_runner.mjs."
        )


def _normalize_params(params: tuple | list | dict | None) -> list | dict:
    if params is None:
        return []
    if isinstance(params, tuple):
        return list(params)
    if isinstance(params, list):
        return params
    if isinstance(params, dict):
        return params
    raise TypeError("params must be a tuple, dict, or None")


def _get_db_key() -> str:
    key = os.getenv(DB_KEY_ENV)
    if not key:
        raise ValueError(
            f"Missing database key. Set the {DB_KEY_ENV} environment variable to enable SQLCipher."
        )
    return key


def _run_node(payload: dict[str, Any]) -> dict[str, Any]:
    """Run the Node DB runner with a JSON payload and return parsed result."""
    _ensure_node_runner()

    # Always include db path and key
    payload = {
        **payload,
        "dbPath": str(DB_PATH),
        "key": _get_db_key(),
    }

    proc = subprocess.run(
        ["node", str(NODE_DB_RUNNER)],
        input=json.dumps(payload).encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if proc.returncode != 0:
        stderr = proc.stderr.decode('utf-8', errors='ignore')
        stdout = proc.stdout.decode('utf-8', errors='ignore')
        raise RuntimeError(
            f"DB runner failed (exit {proc.returncode})\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        )

    try:
        result = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"DB runner returned invalid JSON: {exc}. Output: {proc.stdout!r}"
        ) from exc

    if not result.get("ok", False):
        raise RuntimeError(f"DB runner error: {result.get('error')}")

    return result


def get_connection() -> None:  # kept for backward imports, not used
    raise NotImplementedError(
        "Direct sqlite3 connections are disabled. Use execute_query/execute_dynamic_query."
    )


def init_db() -> None:
    """Initialize DB schema by applying SQL files via the Node runner."""
    # Ensure the parent directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    for subdir in ["tables", "indexes", "triggers", "views"]:
        dir_path: Path = SCHEMA_DIR / subdir
        if not dir_path.exists():
            continue
        for sql_file in sorted(dir_path.glob("*.sql")):
            sql = sql_file.read_text(encoding="utf-8")
            _run_node({"op": "exec", "sql": sql})
            print(f"Applied schema: {sql_file.relative_to(SCHEMA_DIR)}")
    print(f"Database ready at {DB_PATH}")


def execute_query(filename: Path | str, params: tuple | dict | None = None) -> list[tuple]:
    """Load a SQL query from file and execute it with optional parameters via SQLCipher."""
    query_path: Path = QUERIES_DIR / str(filename)
    if not query_path.exists():
        raise FileNotFoundError(f"Query file not found: {query_path}")

    result = _run_node(
        {
            "op": "file",
            "file": str(query_path),
            "params": _normalize_params(params),
        }
    )
    rows = result.get("rows", [])
    return [tuple(row) for row in rows]


def execute_dynamic_query(
    query: Callable[[], str | tuple[str, tuple | dict]],
    params: tuple | dict | None = None,
) -> list[tuple]:
    """Execute a dynamically provided SQL query via SQLCipher."""
    built = query()
    if isinstance(built, tuple) and len(built) == 2:
        sql, query_params = built
        exec_params = _normalize_params(query_params)
    else:
        sql = built  # type: ignore[assignment]
        exec_params = _normalize_params(params)

    result = _run_node({"op": "sql", "sql": sql, "params": exec_params})
    rows = result.get("rows", [])
    return [tuple(row) for row in rows]
