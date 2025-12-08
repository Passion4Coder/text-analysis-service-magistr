from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.analysis.service import (
    process_text,
)
from app.core.database import get_session

router = APIRouter(prefix="/analysis", tags=["Результати 🔍"])


@router.post(
    "/{text_id}/process",
    summary="Проаналізувати текст, витягнути ключові слова, згенерувати summary та зберегти результат",
)
async def process_text_route(
    text_id: int,
    top_n: int = 10,
    diversity: float = 0.5,
    use_semantic_n: bool = False,
    session: AsyncSession = Depends(get_session),
):
    try:
        analysis_result = await process_text(
            session,
            text_id,
            top_n=top_n,
            diversity=diversity,
            use_semantic_n=use_semantic_n,
        )
        return {
            "text_id": analysis_result.text_id,
            "keywords": analysis_result.keywords,
            "summary": analysis_result.summary_text,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
