from fastapi import APIRouter, Query
from app.services.clipboard import clipboard_service
from app.models.clipboard.clipboard_models import Clips, Clip

router = APIRouter(prefix="/clipboard", tags=["Clipboard"])

@router.get("/get_recent_clips")
def get_recent_clips(n: int = Query(10, ge=1)) -> Clips:
    return clipboard_service.get_recent_clips(n)

@router.get("/get_all_clips")
def get_all_clips() -> Clips:
    return clipboard_service.get_all_clips()

@router.post("/add_clip")
def add_clip(clip: Clip) -> None:
    clipboard_service.add_clip(clip.content)

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
def filter_all_clips(search: str = "", time_frame: str = "") -> Clips:
    return clipboard_service.filter_all_clips(search, time_frame)


@router.get("/filter_n_clips")
def filter_n_clips(search: str = "", time_frame: str = "", n: int | None = Query(None, ge=1)) -> Clips:
    return clipboard_service.filter_n_clips(search, time_frame, n)


@router.get("/filter_all_clips_after_id")
def filter_all_clips_after_id(search: str = "", time_frame: str = "", after_id: int = Query(..., ge=0)) -> Clips:
    return clipboard_service.filter_all_clips_after_id(search, time_frame, after_id)


@router.get("/filter_n_clips_before_id")
def filter_n_clips_before_id(
    search: str = "", time_frame: str = "", n: int | None = Query(None, ge=1), before_id: int = Query(..., ge=0)
) -> Clips:
    return clipboard_service.filter_n_clips_before_id(search, time_frame, n, before_id)


@router.get("/get_num_filtered_clips")
def get_num_filtered_clips(search: str = "", time_frame: str = "") -> int:
    return clipboard_service.get_num_filtered_clips(search, time_frame)
