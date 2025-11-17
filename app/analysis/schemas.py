from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional


class AnalysisResultBase(BaseModel):
    text_id: int
    method_id: int
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


class AnalysisRequestTfidf(BaseModel):
    content: str
    top_n: int = 10
    ngram_range: tuple[int, int] = (1, 2)
    max_features: int | None = 5000


class AnalysisRequestRake(BaseModel):
    content: str
    top_n: int = 10


class AnalysisRequestHybrid(BaseModel):
    title: Optional[str] = None
    content: str
    method_name: str = "hybrid"
    text_id: Optional[int] = None
