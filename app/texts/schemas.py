from datetime import datetime

from pydantic import BaseModel


class TextResponse(BaseModel):
    id: int
    title: str
    content: str
    language: str
    source_type: str
    created_at: datetime

    class Config:
        from_attributes = True
