from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional


class AnalysisResultBase(BaseModel):
    text_id: int
    method_id: str
    keywords: List[str]
    definitions: List[Dict[str, str]]
    metrics: Optional[Dict[str, float]] = None


class AnalysisResultCreate(AnalysisResultBase):
    pass


class AnalysisResultRead(AnalysisResultBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
