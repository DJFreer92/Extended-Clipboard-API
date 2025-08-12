from pydantic import BaseModel
from typing import Optional, List


class Clip(BaseModel):
    id: int
    content: str
    from_app_name: Optional[str] = None
    tags: List[str] = []
    timestamp: str


class Clips(BaseModel):
    clips: list[Clip]


class Tag(BaseModel):
    id: int
    name: str


class Tags(BaseModel):
    tags: list[Tag]


class FavoriteClipIDs(BaseModel):
    clip_ids: list[int]
