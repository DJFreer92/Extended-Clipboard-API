"""
Pytest bootstrap to make imports work consistently.

Strategy:
- Add the repository root to sys.path so we can import the package as 'app'.
- Import 'app' and alias its subpackages ('api', 'services', 'models', 'db', 'core')
    to top-level module names to satisfy modules that expect PYTHONPATH=app.
    This also allows relative imports inside app.db (e.g., from ..core) to work.
"""
from __future__ import annotations

import sys
from pathlib import Path
import os
import pytest


def _bootstrap_imports() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    # Import app as a proper package
    import importlib

    app_pkg = importlib.import_module("app")

    # Import subpackages so they exist in sys.modules under 'app.*'
    app_api = importlib.import_module("app.api")
    app_services = importlib.import_module("app.services")
    app_models = importlib.import_module("app.models")
    app_db = importlib.import_module("app.db")
    app_core = importlib.import_module("app.core")

    # Also load app.db.db so its relative imports resolve during module import
    app_db_db = importlib.import_module("app.db.db")

    # Create top-level aliases to support modules that expect PYTHONPATH=app
    sys.modules.setdefault("api", app_api)
    sys.modules.setdefault("services", app_services)
    sys.modules.setdefault("models", app_models)
    sys.modules.setdefault("db", app_db)
    sys.modules.setdefault("core", app_core)

    # Map 'db.db' to the loaded 'app.db.db' module so 'from db.db import ...' works
    sys.modules.setdefault("db.db", app_db_db)


_bootstrap_imports()

# Ensure an encryption key exists for SQLCipher during tests
os.environ.setdefault("CLIPBOARD_DB_KEY", "test-secret-key")

# Enforce encrypted mode during tests; no plaintext bypass.


@pytest.fixture(scope="session", autouse=True)
def require_sqlcipher_available() -> None:
    """Skip the entire test session if SQLCipher is not available in better-sqlite3.

    This maintains the encryption-only guarantee without forcing developers/CI
    to rebuild better-sqlite3 during collection. When SQLCipher is present,
    the tests will run normally and exercise encrypted DB operations.
    """
    try:
        # defer import until after sys.path bootstrap
        from app.db.db import _run_node  # type: ignore
        # Try a no-op exec which will fail early in the Node runner if SQLCipher is missing
        _run_node({"op": "exec", "sql": "PRAGMA user_version = 0;"})
    except Exception as exc:  # broad: surface clear skip reasons
        msg = str(exc)
        if "SQLCipher not available" in msg or "Missing database key" in msg:
            pytest.skip(
                "SQLCipher not available in better-sqlite3 build (or key missing). "
                "Encrypted-only mode enforced; skipping tests on this environment.",
                allow_module_level=True,
            )
        # For other unexpected errors, let tests fail normally
