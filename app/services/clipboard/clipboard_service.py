from collections.abc import Mapping
from app.models.clipboard.clipboard_models import *
from app.core.constants import (
    GET_N_CLIPS,
    GET_ALL_CLIPS,
    ADD_CLIP,
    DELETE_CLIP,
    DELETE_ALL_CLIPS,
    GET_ALL_CLIPS_AFTER_ID,
    GET_N_CLIPS_BEFORE_ID,
    GET_NUM_CLIPS,
    ADD_CLIP_WITH_TIMESTAMP,
)
from app.db.db import execute_query, execute_dynamic_query
from app.db.queries.filter_clips_dynamic_queries import (
    filter_all_clips_query,
    filter_n_clips_query,
    filter_all_clips_after_id_query,
    filter_n_clips_before_id_query,
    get_num_filtered_clips_query,
)


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


# New static queries
def get_all_clips_after_id(before_id: int) -> Clips:
    rows = execute_query(GET_ALL_CLIPS_AFTER_ID, {"before_id": before_id})
    return Clips(clips=[_row_to_clip(r) for r in rows])


def get_n_clips_before_id(n: int | None, before_id: int) -> Clips:
    rows = execute_query(GET_N_CLIPS_BEFORE_ID, {"n": n, "before_id": before_id})
    return Clips(clips=[_row_to_clip(r) for r in rows])


def get_num_clips() -> int:
    rows = execute_query(GET_NUM_CLIPS)
    return int(rows[0][0]) if rows else 0


def add_clip_with_timestamp(content: str, timestamp: str) -> None:
    execute_query(ADD_CLIP_WITH_TIMESTAMP, {"content": content, "timestamp": timestamp})


# Dynamic filter queries
def filter_all_clips(search: str = "", time_frame: str = "") -> Clips:
    rows = execute_dynamic_query(lambda: filter_all_clips_query(search=search, time_frame=time_frame))
    return Clips(clips=[_row_to_clip(r) for r in rows])


def filter_n_clips(search: str = "", time_frame: str = "", n: int | None = None) -> Clips:
    rows = execute_dynamic_query(
        lambda: filter_n_clips_query(search=search, time_frame=time_frame, n=n)
    )
    return Clips(clips=[_row_to_clip(r) for r in rows])


def filter_all_clips_after_id(search: str = "", time_frame: str = "", after_id: int = 0) -> Clips:
    rows = execute_dynamic_query(
        lambda: filter_all_clips_after_id_query(search=search, time_frame=time_frame, after_id=after_id)
    )
    return Clips(clips=[_row_to_clip(r) for r in rows])


def filter_n_clips_before_id(
    search: str = "", time_frame: str = "", n: int | None = None, before_id: int = 0
) -> Clips:
    rows = execute_dynamic_query(
        lambda: filter_n_clips_before_id_query(
            search=search, time_frame=time_frame, n=n, before_id=before_id
        )
    )
    return Clips(clips=[_row_to_clip(r) for r in rows])


def get_num_filtered_clips(search: str = "", time_frame: str = "") -> int:
    rows = execute_dynamic_query(lambda: get_num_filtered_clips_query(search=search, time_frame=time_frame))
    return int(rows[0][0]) if rows else 0
