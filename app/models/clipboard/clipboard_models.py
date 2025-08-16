from pydantic import BaseModel
from typing import Optional, List


class Clip(BaseModel):
    id: int
    content: str
    from_app_name: Optional[str] = None
    tags: List[str] = []
    timestamp: str
    is_favorite: bool = False


class ClipInput(BaseModel):
    """Input model for adding clips - timestamp is optional."""
    content: str
    from_app_name: Optional[str] = None
    tags: List[str] = []
    timestamp: Optional[str] = None
    is_favorite: bool = False


class Clips(BaseModel):
    clips: list[Clip]


class Tag(BaseModel):
    id: int
    name: str


class Tags(BaseModel):
    tags: list[Tag]


class FavoriteClipIDs(BaseModel):
    clip_ids: list[int]
