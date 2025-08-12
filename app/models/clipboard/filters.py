from pydantic import BaseModel

class Filters(BaseModel):
    search: str = ''
    time_frame: str = ''
    selected_tags: list[str] = []
    favorites_only: bool = False
