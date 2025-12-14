from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.analysis.service import get_analysis_result_by_id, get_analysis_results, process_text
from app.core.database import get_session

router = APIRouter(prefix="/analysis", tags=["Результати 🔍"])


@router.get("", summary="Отримати список всіх результатів")
async def get(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
):
    return await get_analysis_results(session, page, page_size)


@router.get("/{id}", summary="Отримати результат за id")
async def get_by_id(id: int, session: AsyncSession = Depends(get_session)):
    analysis_result = await get_analysis_result_by_id(session, id)

    if not analysis_result:
        raise HTTPException(status_code=404, detail="Результат не знайдено.")

    return analysis_result


@router.post(
    "/{text_id}/process",
    summary="Проаналізувати текст, витягнути ключові слова, згенерувати summary та зберегти результат",
)
async def process_text_route(
    text_id: int,
    top_n: int = Query(10, ge=1, le=25),
    diversity: float = Query(1, ge=0, le=1),
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
