from __future__ import annotations

"""
Seed the SQLite database with sample Clips.

- Inserts 100 clips with unique content.
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
from app.core.constants import (
    QUERIES_DIR,
    DB_PATH,
    ADD_TAG_IF_NOT_EXISTS,
    ADD_CLIP_TAG,
    ADD_FAVORITE,
    GET_LAST_CLIP_ID,
)

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


def _maybe_add_tags_and_favorite(clip_id: int, possible_tags: list[str], tag_chance: float = 0.5, fav_chance: float = 0.15) -> None:
    """Randomly assign 0..N tags and maybe favorite to a clip.

    tag_chance: probability per tag to be considered for assignment.
    fav_chance: probability to mark as favorite.
    """
    # Decide tags
    chosen = [t for t in possible_tags if random.random() < tag_chance]
    for tag in chosen:
        execute_query(ADD_TAG_IF_NOT_EXISTS, {"tag_name": tag})
        execute_query(ADD_CLIP_TAG, {"clip_id": clip_id, "tag_name": tag})
    # Maybe favorite
    if random.random() < fav_chance:
        execute_query(ADD_FAVORITE, {"clip_id": clip_id})


def seed(n: int = 100) -> None:
    # Ensure DB exists and schema is applied
    init_db()

    # Precompute timestamps oldest→newest and insert in that order
    timestamps = _sorted_random_timestamps(n, 2)

    app_names = ["Safari", "Chrome", "VSCode", "Terminal", "Notes", "Mail", None]
    tag_pool = ["work", "personal", "todo", "idea", "code", "quote", "ref"]

    # Insert n clips (collect assigned IDs after each insert using MAX(ID))
    # Fetch current max ID beforehand for display purposes
    starting_rows = execute_query("get_all_clips.sql")
    start_count = len(starting_rows)

    for i, ts in enumerate(timestamps, start=1):
        base_token = random.randint(10000, 999999)
        content = (
            f"Seeded clip #{start_count + i} — {random.choice(['alpha', 'beta', 'gamma', 'delta', 'epsilon'])}"
            f" — token:{base_token}"
        )
        from_app = random.choice(app_names)
        execute_query(ADD_WITH_TS, {"content": content, "timestamp": ts, "from_app_name": from_app})
        # Fetch the most recent clip id via file-based query (connection-safe)
        last_id_row = execute_query(GET_LAST_CLIP_ID)
        if not last_id_row:
            raise RuntimeError("No clip ID returned after insert; database may be misconfigured.")
        clip_id = int(last_id_row[0][0])
        _maybe_add_tags_and_favorite(clip_id, tag_pool)

    # Report final count
    rows = execute_query("get_all_clips.sql")
    print(f"Seed complete. Inserted {n} clips. Current row count: {len(rows)}. DB at {DB_PATH}")


if __name__ == "__main__":
    seed()
