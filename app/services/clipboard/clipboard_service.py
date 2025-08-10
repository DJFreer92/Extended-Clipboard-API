from collections.abc import Mapping
from app.models.clipboard.clipboard_models import *
from app.core.constants import GET_N_CLIPS, GET_ALL_CLIPS, ADD_CLIP, DELETE_CLIP, DELETE_ALL_CLIPS
from app.db.db import execute_query


def _row_to_clip(row: Mapping | tuple) -> Clip:
    """Map a DB row (tuple or mapping) to a Clip model.

    - DB rows from sqlite3 without row_factory are tuples in column order (ID, Content, Timestamp).
    - In tests/mocks we sometimes receive dict-like rows with various key casings.
    """
    if isinstance(row, tuple) or isinstance(row, list):
        return Clip(id=int(row[0]), content=str(row[1]), timestamp=str(row[2]))

    # Treat as mapping; be case-insensitive on keys
    keys = {str(k).lower(): k for k in row.keys()}  # original key by lowercase alias
    id_key = keys.get("id")
    content_key = keys.get("content")
    ts_key = keys.get("timestamp")
    return Clip(id=int(row[id_key]), content=str(row[content_key]), timestamp=str(row[ts_key]))

def get_recent_clips(n: int | None) -> Clips:
    result = execute_query(GET_N_CLIPS, {"n": n})
    clips = Clips(clips=[_row_to_clip(r) for r in result])
    return clips

def get_all_clips() -> Clips:
    result = execute_query(GET_ALL_CLIPS)
    clips = Clips(clips=[_row_to_clip(r) for r in result])
    return clips

def add_clip(content: str) -> None:
    execute_query(ADD_CLIP, {"content": content})

def delete_clip(id: int) -> None:
    execute_query(DELETE_CLIP, (id,))

def delete_all_clips() -> None:
    execute_query(DELETE_ALL_CLIPS)
