from pydantic import BaseModel

class Clip(BaseModel):
	content: str

class Clips(BaseModel):
    clips: list[Clip]
