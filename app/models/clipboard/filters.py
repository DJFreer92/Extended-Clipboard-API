from pydantic import BaseModel

class Filters(BaseModel):
    search: str = ''
    selected_apps: list[str] = []
    selected_tags: list[str] = []
    favorites_only: bool = False
    time_frame: str = ''
