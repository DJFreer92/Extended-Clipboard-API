from __future__ import annotations

from uvicorn import run
import os

# Ensure the repository root is on sys.path so 'app' package imports resolve
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
	sys.path.insert(0, str(repo_root))

if __name__ == "__main__":
	# Bind to localhost only; pass import string so reload works without warnings
	run("app.api.main:app", host="127.0.0.1", port=8000, reload=True)
