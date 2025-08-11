from __future__ import annotations

"""
Seed the SQLite database with sample Clips.

- Inserts 1000 clips with unique content.
- Timestamps are distributed randomly over the last 2 years.
- Uses the project's DB helper and SQL files (no inline SQL).

Run directly:
    python scripts/seed_db.py
"""

from datetime import datetime, timedelta
import random

# Ensure we can import the app package when running as a script
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from app.db.db import execute_query, init_db
from app.core.constants import QUERIES_DIR, DB_PATH

ADD_WITH_TS = QUERIES_DIR / "add_clip_with_timestamp.sql"


def _sorted_random_timestamps(n: int, years: int = 2) -> list[str]:
    """Generate n random timestamps over the past `years` years, sorted oldest→newest."""
    now = datetime.now()
    earliest = now - timedelta(days=365 * years)
    total_seconds = int((now - earliest).total_seconds())
    offsets = [random.randint(0, total_seconds) for _ in range(n)]
    offsets.sort()  # ensures we insert oldest first, newest last
    return [
        (earliest + timedelta(seconds=o)).strftime("%Y-%m-%d %H:%M:%S")
        for o in offsets
    ]


def seed(n: int = 1000) -> None:
    # Ensure DB exists and schema is applied
    init_db()

    # Precompute timestamps oldest→newest and insert in that order
    timestamps = _sorted_random_timestamps(n, 2)

    # Insert n clips
    for i, ts in enumerate(timestamps, start=1):
        content = f"Seeded clip #{i} — {random.choice(['alpha', 'beta', 'gamma', 'delta', 'epsilon'])}"
        # ensure slight content variability to avoid trigger deletion
        content += f" — token:{random.randint(100000, 999999)}"
        execute_query(ADD_WITH_TS, {"content": content, "timestamp": ts})

    # Report final count
    rows = execute_query("get_all_clips.sql")
    print(f"Seed complete. Inserted ~{n} clips. Current row count: {len(rows)}. DB at {DB_PATH}")


if __name__ == "__main__":
    seed(1000)
