from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TextResponse(BaseModel):
    id: int
    title: Optional[str]
    content: str
    language: str
    source_type: str
    created_at: datetime

    class Config:
        from_attributes = True
