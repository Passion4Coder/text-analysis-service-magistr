from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional


class NoteBase(BaseModel):
    text_id: int
    analysis_result_id: int
    structure: Dict
    summary: Optional[str] = None


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
