from models.clipboard.clipboard_models import *
from app.core.constants import GET_N_CLIPS, GET_ALL_CLIPS, ADD_CLIP, DELETE_CLIP, DELETE_ALL_CLIPS
from db.db import execute_query

def get_recent_clips(n: int | None) -> Clips:
    result: list[dict] = execute_query(GET_N_CLIPS, (n,))
    clips: Clips = Clips([Clip(**clip) for clip in result])
    return clips

def get_all_clips() -> Clips:
    result: list[dict] = execute_query(GET_ALL_CLIPS)
    clips: Clips = Clips([Clip(**clip) for clip in result])
    return clips

def add_clip(content: str) -> None:
    execute_query(ADD_CLIP, (content,))

def delete_clip(id: int) -> None:
    execute_query(DELETE_CLIP, (id,))

def delete_all_clips() -> None:
    execute_query(DELETE_ALL_CLIPS)
