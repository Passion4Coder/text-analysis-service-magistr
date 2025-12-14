from typing import List

from pydantic import BaseModel


class KeywordCountStats(BaseModel):
    n_user: int
    n_semantic_recommended: int
    n_final: int


class DiversityPerformanceStats(BaseModel):
    diversity: float
    avg_keybert_ms: float
    avg_llm_ms: float


class StatsResponse(BaseModel):
    keyword_count: List[KeywordCountStats]
    diversity_performance: List[DiversityPerformanceStats]
    analysis_duration: List[float]
