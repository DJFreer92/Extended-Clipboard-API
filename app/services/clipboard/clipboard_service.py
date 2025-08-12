from collections.abc import Mapping
from typing import Sequence, Any

from app.models.clipboard.clipboard_models import (
    Clip,
    Clips,
    Tags,
    Tag,
    FavoriteClipIDs,
)
from app.models.clipboard.filters import Filters
from app.core.constants import (
    GET_N_CLIPS,
    GET_ALL_CLIPS,
    ADD_CLIP,
    DELETE_CLIP,
    DELETE_ALL_CLIPS,
    DELETE_FAVORITE_FOR_CLIP,
    GET_TAG_IDS_FOR_CLIP,
    DELETE_CLIP_TAGS_FOR_CLIP,
    DELETE_UNUSED_TAG,
    DELETE_ALL_CLIP_TAGS,
    DELETE_ALL_FAVORITES,
    DELETE_ALL_TAGS,
    GET_ALL_CLIPS_AFTER_ID,
    GET_N_CLIPS_BEFORE_ID,
    GET_NUM_CLIPS,
    ADD_CLIP_WITH_TIMESTAMP,
    ADD_CLIP_TAG,
    REMOVE_CLIP_TAG,
    GET_ALL_TAGS,
    GET_NUM_CLIPS_PER_TAG,
    ADD_FAVORITE,
    REMOVE_FAVORITE,
    GET_ALL_FAVORITES,
    GET_NUM_FAVORITES,
    ADD_TAG_IF_NOT_EXISTS,
    GET_ALL_FROM_APPS,
)
from app.db.db import execute_query, execute_dynamic_query
from app.db.queries.filter_clips_dynamic_queries import (
    filter_all_clips_query,
    filter_n_clips_query,
    filter_all_clips_after_id_query,
    filter_n_clips_before_id_query,
    get_num_filtered_clips_query,
)


def _row_to_clip(row: Mapping | Sequence[Any]) -> Clip:
    """Map a DB row (tuple/sequence) or mapping to Clip.

    Supports legacy 5-column shape and new 6-column shape with IsFavorite.
    Tuple/list layout (new): (ClipID, Content, FromAppName, TagsCSV, Timestamp, IsFavorite)
    """
    if isinstance(row, (tuple, list)):
        clip_id = int(row[0])
        content = str(row[1])
        from_app = row[2] if len(row) > 2 else None
        tags_csv = row[3] if len(row) > 3 else None
        timestamp = str(row[4]) if len(row) > 4 else str(row[-1])
        is_favorite = bool(row[5]) if len(row) > 5 else False
        tags_list = [t for t in str(tags_csv).split(",") if t] if tags_csv else []
        return Clip(
            id=clip_id,
            content=content,
            from_app_name=from_app,
            tags=tags_list,
            timestamp=timestamp,
            is_favorite=is_favorite,
        )

    keys = {str(k).lower(): k for k in row.keys()}
    id_key = keys.get("clipid") or keys.get("id")
    content_key = keys.get("content")
    from_app_key = keys.get("fromappname")
    tags_key = keys.get("tags")
    ts_key = keys.get("timestamp")
    fav_key = keys.get("isfavorite") or keys.get("favorite")
    tags_val = row.get(tags_key) if tags_key else None  # type: ignore[index]
    tags_list = [t for t in str(tags_val).split(",") if t] if tags_val else []
    is_fav_val = bool(row.get(fav_key)) if fav_key and fav_key in row else False  # type: ignore[index]
    return Clip(
        id=int(row[id_key]),  # type: ignore[index]
        content=str(row[content_key]),  # type: ignore[index]
        from_app_name=row.get(from_app_key) if from_app_key else None,  # type: ignore[index]
        tags=tags_list,
        timestamp=str(row[ts_key]),  # type: ignore[index]
        is_favorite=is_fav_val,
    )

def get_recent_clips(n: int | None) -> Clips:
    result = execute_query(GET_N_CLIPS, {"n": n})
    clips = Clips(clips=[_row_to_clip(r) for r in result])
    return clips

def get_all_clips() -> Clips:
    result = execute_query(GET_ALL_CLIPS)
    clips = Clips(clips=[_row_to_clip(r) for r in result])
    return clips

def add_clip(content: str, from_app_name: str | None = None) -> None:
    execute_query(ADD_CLIP, {"content": content, "from_app_name": from_app_name})

def delete_clip(id: int) -> None:
    # Remove favorite if present
    execute_query(DELETE_FAVORITE_FOR_CLIP, {"clip_id": id})
    # Gather tag ids
    tag_rows = execute_query(GET_TAG_IDS_FOR_CLIP, {"clip_id": id})
    # Remove clip tag mappings
    execute_query(DELETE_CLIP_TAGS_FOR_CLIP, {"clip_id": id})
    # Remove unused tags
    for (tag_id,) in tag_rows:
        execute_query(DELETE_UNUSED_TAG, {"tag_id": tag_id})
    # Finally delete clip
    execute_query(DELETE_CLIP, {"clip_id": id})

def delete_all_clips() -> None:
    # Ordered to avoid FK-like leftover references
    execute_query(DELETE_ALL_CLIP_TAGS)
    execute_query(DELETE_ALL_FAVORITES)
    execute_query(DELETE_ALL_CLIPS)
    execute_query(DELETE_ALL_TAGS)


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


def add_clip_with_timestamp(content: str, timestamp: str, from_app_name: str | None = None) -> None:
    execute_query(
        ADD_CLIP_WITH_TIMESTAMP,
        {"content": content, "timestamp": timestamp, "from_app_name": from_app_name},
    )


# Dynamic filter queries
def _ensure_filters(
    search: str = "",
    time_frame: str = "",
    selected_tags: list[str] | None = None,
    selected_apps: list[str] | None = None,
    favorites_only: bool = False,
) -> Filters:
    return Filters(
        search=search,
        time_frame=time_frame,
        selected_tags=selected_tags or [],
        favorites_only=favorites_only,
        selected_apps=selected_apps or [],
    )


def filter_all_clips(
    search: str = "",
    time_frame: str = "",
    selected_tags: list[str] | None = None,
    selected_apps: list[str] | None = None,
    favorites_only: bool = False,
) -> Clips:
    filters = _ensure_filters(
        search=search,
        time_frame=time_frame,
        selected_tags=selected_tags,
        selected_apps=selected_apps,
        favorites_only=favorites_only,
    )
    rows = execute_dynamic_query(lambda: filter_all_clips_query(filters))
    return Clips(clips=[_row_to_clip(r) for r in rows])


def filter_n_clips(
    search: str = "",
    time_frame: str = "",
    n: int | None = None,
    selected_tags: list[str] | None = None,
    selected_apps: list[str] | None = None,
    favorites_only: bool = False,
) -> Clips:
    filters = Filters(
        search=search,
        time_frame=time_frame,
        selected_tags=selected_tags or [],
    favorites_only=favorites_only,
    selected_apps=selected_apps or [],
    )
    rows = execute_dynamic_query(lambda: filter_n_clips_query(filters, n=n))
    return Clips(clips=[_row_to_clip(r) for r in rows])


def filter_all_clips_after_id(
    search: str = "",
    time_frame: str = "",
    after_id: int = 0,
    selected_tags: list[str] | None = None,
    selected_apps: list[str] | None = None,
    favorites_only: bool = False,
) -> Clips:
    filters = Filters(
        search=search,
        time_frame=time_frame,
        selected_tags=selected_tags or [],
    favorites_only=favorites_only,
    selected_apps=selected_apps or [],
    )
    rows = execute_dynamic_query(lambda: filter_all_clips_after_id_query(filters, after_id=after_id))
    return Clips(clips=[_row_to_clip(r) for r in rows])


def filter_n_clips_before_id(
    search: str = "",
    time_frame: str = "",
    n: int | None = None,
    before_id: int = 0,
    selected_tags: list[str] | None = None,
    selected_apps: list[str] | None = None,
    favorites_only: bool = False,
) -> Clips:
    filters = Filters(
        search=search,
        time_frame=time_frame,
        selected_tags=selected_tags or [],
    favorites_only=favorites_only,
    selected_apps=selected_apps or [],
    )
    rows = execute_dynamic_query(
        lambda: filter_n_clips_before_id_query(
            filters, n=n, before_id=before_id
        )
    )
    return Clips(clips=[_row_to_clip(r) for r in rows])


def get_num_filtered_clips(
    search: str = "",
    time_frame: str = "",
    selected_tags: list[str] | None = None,
    selected_apps: list[str] | None = None,
    favorites_only: bool = False,
) -> int:
    filters = Filters(
        search=search,
        time_frame=time_frame,
        selected_tags=selected_tags or [],
    favorites_only=favorites_only,
    selected_apps=selected_apps or [],
    )
    rows = execute_dynamic_query(lambda: get_num_filtered_clips_query(filters))
    return int(rows[0][0]) if rows else 0


# Tag methods
def add_clip_tag(clip_id: int, tag_name: str) -> None:
    # Ensure tag row exists first, then map
    execute_query(ADD_TAG_IF_NOT_EXISTS, {"tag_name": tag_name})
    execute_query(ADD_CLIP_TAG, {"clip_id": clip_id, "tag_name": tag_name})


def remove_clip_tag(clip_id: int, tag_id: int) -> None:
    execute_query(REMOVE_CLIP_TAG, {"clip_id": clip_id, "tag_id": tag_id})
    execute_query(DELETE_UNUSED_TAG, {"tag_id": tag_id})


def get_all_tags() -> Tags:
    rows = execute_query(GET_ALL_TAGS)
    return Tags(tags=[Tag(id=int(r[0]), name=str(r[1])) for r in rows])


def get_num_clips_per_tag(tag_id: int) -> int:
    rows = execute_query(GET_NUM_CLIPS_PER_TAG, {"tag_id": tag_id})
    return int(rows[0][0]) if rows else 0


# Favorites methods
def add_favorite(clip_id: int) -> None:
    execute_query(ADD_FAVORITE, {"clip_id": clip_id})


def remove_favorite(clip_id: int) -> None:
    execute_query(REMOVE_FAVORITE, {"clip_id": clip_id})


def get_all_favorites() -> FavoriteClipIDs:
    rows = execute_query(GET_ALL_FAVORITES)
    return FavoriteClipIDs(clip_ids=[int(r[0]) for r in rows])


def get_num_favorites() -> int:
    rows = execute_query(GET_NUM_FAVORITES)
    return int(rows[0][0]) if rows else 0


# From apps
def get_all_from_apps() -> list[str]:
    rows = execute_query(GET_ALL_FROM_APPS)
    # Rows may contain None (clips without app); include as None or filter out? We'll keep non-null only for cleanliness.
    apps = [r[0] for r in rows if r[0] is not None]
    return apps
