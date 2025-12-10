from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.texts.schemas import TextResponse
from app.texts.service import get_text_by_id, get_texts

router = APIRouter(prefix="/texts", tags=["Тексти 📄"])


@router.get("", summary="Отримати список всіх текстів")
async def get(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=2),
    session: AsyncSession = Depends(get_session),
):
    return await get_texts(session, page, page_size)


@router.get("/{text_id}", response_model=TextResponse, summary="Отримати текст за id")
async def get_by_id(text_id: int, session: AsyncSession = Depends(get_session)):
    text = await get_text_by_id(session, text_id)

    if not text:
        raise HTTPException(status_code=404, detail="Текст не знайдено.")

    return text
