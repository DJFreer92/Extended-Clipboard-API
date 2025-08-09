from fastapi import APIRouter, Query
from app.services.clipboard import clipboard_service
from app.models.clipboard.clipboard_models import Clips, Clip

router = APIRouter(prefix="/clipboard", tags=["Clipboard"])

@router.get("/get_recent_clips")
def get_recent_clips(n: int = Query(10, ge=1)) -> Clips:
    return clipboard_service.get_recent_clips(n)

@router.post("/add_clip")
def add_clip(clip: Clip) -> None:
    clipboard_service.add_clip(clip.content)
