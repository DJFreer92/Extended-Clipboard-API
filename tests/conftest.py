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
