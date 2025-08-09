from pydantic import BaseModel

class Clip(BaseModel):
    id: int
    content: str
    timestamp: str

class Clips(BaseModel):
    clips: list[Clip]
