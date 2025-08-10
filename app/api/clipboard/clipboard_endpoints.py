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
