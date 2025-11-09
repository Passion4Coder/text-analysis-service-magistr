from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from analysis.service import analyze_and_save

router = APIRouter(prefix="/analysis", tags=["Analysis"])


class AnalysisRequest(BaseModel):
    title: Optional[str] = None
    content: str
    method_name: str = "hybrid"
    text_id: Optional[int] = None


@router.post("/hybrid")
async def analyze_text(data: AnalysisRequest):
    result = await analyze_and_save(
        content=data.content,
        title=data.title,
        text_id=data.text_id,
        method_name=data.method_name,
    )
    return result
