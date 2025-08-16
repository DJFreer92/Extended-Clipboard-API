from fastapi import APIRouter, Query
from app.services.clipboard import clipboard_service
from app.models.clipboard.clipboard_models import Clips, Clip, ClipInput

router = APIRouter(prefix="/clipboard", tags=["Clipboard"])

@router.get("/get_recent_clips")
def get_recent_clips(n: int = Query(10, ge=1)) -> Clips:
    return clipboard_service.get_recent_clips(n)

@router.get("/get_all_clips")
def get_all_clips() -> Clips:
    return clipboard_service.get_all_clips()

@router.post("/add_clip")
def add_clip(clip: ClipInput, from_app_name: str | None = None) -> None:
    # Use timestamp from clip if provided, otherwise service will generate UTC timestamp
    clipboard_service.add_clip_with_timestamp_support(
        content=clip.content,
        timestamp=clip.timestamp,
        from_app_name=from_app_name or clip.from_app_name
    )

@router.post("/delete_clip")
def delete_clip(id: int) -> None:
    clipboard_service.delete_clip(id)

@router.post("/delete_all_clips")
def delete_all_clips() -> None:
    clipboard_service.delete_all_clips()


# New endpoints: static queries
@router.get("/get_all_clips_after_id")
def get_all_clips_after_id(before_id: int = Query(..., ge=0)) -> Clips:
    return clipboard_service.get_all_clips_after_id(before_id)


@router.get("/get_n_clips_before_id")
def get_n_clips_before_id(n: int | None = Query(None, ge=1), before_id: int = Query(..., ge=0)) -> Clips:
    return clipboard_service.get_n_clips_before_id(n, before_id)


@router.get("/get_num_clips")
def get_num_clips() -> int:
    return clipboard_service.get_num_clips()


# New endpoints: dynamic filter queries
@router.get("/filter_all_clips")
def filter_all_clips(
    search: str = "",
    time_frame: str = "",
    selected_tags: list[str] = Query(default=[]),
    selected_apps: list[str] = Query(default=[]),
    favorites_only: bool = False,
) -> Clips:
    return clipboard_service.filter_all_clips(search, time_frame, selected_tags, selected_apps, favorites_only)


@router.get("/filter_n_clips")
def filter_n_clips(
    search: str = "",
    time_frame: str = "",
    n: int | None = Query(None, ge=1),
    selected_tags: list[str] = Query(default=[]),
    selected_apps: list[str] = Query(default=[]),
    favorites_only: bool = False,
) -> Clips:
    return clipboard_service.filter_n_clips(search, time_frame, n, selected_tags, selected_apps, favorites_only)


@router.get("/filter_all_clips_after_id")
def filter_all_clips_after_id(
    search: str = "",
    time_frame: str = "",
    after_id: int = Query(..., ge=0),
    selected_tags: list[str] = Query(default=[]),
    selected_apps: list[str] = Query(default=[]),
    favorites_only: bool = False,
) -> Clips:
    return clipboard_service.filter_all_clips_after_id(search, time_frame, after_id, selected_tags, selected_apps, favorites_only)


@router.get("/filter_n_clips_before_id")
def filter_n_clips_before_id(
    search: str = "",
    time_frame: str = "",
    n: int | None = Query(None, ge=1),
    before_id: int = Query(..., ge=0),
    selected_tags: list[str] = Query(default=[]),
    selected_apps: list[str] = Query(default=[]),
    favorites_only: bool = False,
) -> Clips:
    return clipboard_service.filter_n_clips_before_id(search, time_frame, n, before_id, selected_tags, selected_apps, favorites_only)


@router.get("/get_num_filtered_clips")
def get_num_filtered_clips(
    search: str = "",
    time_frame: str = "",
    selected_tags: list[str] = Query(default=[]),
    selected_apps: list[str] = Query(default=[]),
    favorites_only: bool = False,
) -> int:
    return clipboard_service.get_num_filtered_clips(search, time_frame, selected_tags, selected_apps, favorites_only)


# Tag endpoints
@router.post("/add_clip_tag")
def add_clip_tag(clip_id: int, tag_name: str) -> None:
    clipboard_service.add_clip_tag(clip_id, tag_name)


@router.post("/remove_clip_tag")
def remove_clip_tag(clip_id: int, tag_id: int) -> None:
    clipboard_service.remove_clip_tag(clip_id, tag_id)


@router.get("/get_all_tags")
def get_all_tags():
    return clipboard_service.get_all_tags()


@router.get("/get_num_clips_per_tag")
def get_num_clips_per_tag(tag_id: int) -> int:
    return clipboard_service.get_num_clips_per_tag(tag_id)


# Favorite endpoints
@router.post("/add_favorite")
def add_favorite(clip_id: int) -> None:
    clipboard_service.add_favorite(clip_id)


@router.post("/remove_favorite")
def remove_favorite(clip_id: int) -> None:
    clipboard_service.remove_favorite(clip_id)


@router.get("/get_all_favorites")
def get_all_favorites():
    return clipboard_service.get_all_favorites()


@router.get("/get_num_favorites")
def get_num_favorites() -> int:
    return clipboard_service.get_num_favorites()


@router.get("/get_all_from_apps")
def get_all_from_apps() -> list[str]:
    return clipboard_service.get_all_from_apps()
