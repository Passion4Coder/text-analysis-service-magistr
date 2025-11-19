from pydantic import BaseModel
from typing import List


class MetricsByMethod(BaseModel):
    method_name: str
    precision: float
    recall: float
    f1_score: float


class MetricsOverTime(BaseModel):
    date: str
    method_name: str
    f1_score: float


class GraphsResponse(BaseModel):
    precision_comparison: List[MetricsByMethod]
    recall_comparison: List[MetricsByMethod]
    f1_comparison: List[MetricsByMethod]
    f1_over_time: List[MetricsOverTime]
