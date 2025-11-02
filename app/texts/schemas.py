from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TextBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    language: str = "uk"
    source_type: str = "manual_upload"


class TextCreate(TextBase):
    pass


class TextRead(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
