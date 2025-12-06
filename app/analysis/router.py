from fastapi import APIRouter, Depends, HTTPException
from app.analysis.service import (
    process_text,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_factory


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


router = APIRouter(prefix="/analysis", tags=["Результати 🔍"])


# @router.get(
#     "/list",
#     summary="Отримати список усіх проаналізованих текстів",
#     response_model=AnalysisResultList,
# )
# async def get_analysis_list():
#     analyses = await fetch_all_analyses()
#     return {"count": len(analyses), "items": analyses}


# @router.get(
#     "/{text_id}",
#     summary="Отримати повний результат аналізу",
#     response_model=AnalysisResultRead,
# )
# async def get_analysis(text_id: int):
#     analysis = await fetch_analysis_by_text_id(text_id)

#     if analysis is None:
#         raise HTTPException(status_code=404, detail="Аналіз не знайдено.")

#     return analysis


# @router.get("/{text_id}/keywords", summary="Отримати лише ключові слова")
# async def get_keywords_only(text_id: int):
#     analysis = await fetch_analysis_by_text_id(text_id)

#     if analysis is None:
#         raise HTTPException(status_code=404, detail="Аналіз не знайдено.")

#     return {"keywords": analysis.get("keywords", [])}


@router.post(
    "/{text_id}/process",
    summary="Проаналізувати текст, витягнути ключові слова та зберегти результат",
)
async def process_text_route(
    text_id: int,
    top_n: int = 10,
    diversity: float = 0.5,
    session: AsyncSession = Depends(get_session),
):
    try:
        analysis_result = await process_text(
            session, text_id, top_n=top_n, diversity=diversity
        )
        return {
            "text_id": analysis_result.text_id,
            "keywords": analysis_result.keywords,
            "lemmas": analysis_result.lemmas,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
