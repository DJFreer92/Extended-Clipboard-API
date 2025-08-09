from app.models.clipboard.clipboard_models import *
from app.core.db_constants import GET_N_CLIPS, ADD_CLIP
from app.core.db import execute_query

def get_recent_clips(n: int | None) -> Clips:
    result: list[dict] = execute_query(GET_N_CLIPS, (n,))
    clips: list[Clip] = [Clip(content=clip['content']) for clip in result]
    return Clips(clips=clips)

def add_clip(content: str) -> None:
    execute_query(ADD_CLIP, (content,))
