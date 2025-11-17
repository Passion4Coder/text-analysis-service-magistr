from fastapi import APIRouter, HTTPException
from typing import List

from app.texts.schemas import TextRead
from app.texts.service import get_all_texts, get_text_by_id

router = APIRouter(prefix="/texts", tags=["Тексти 📄"])


@router.get("/", response_model=List[TextRead], summary="Отримати список всіх текстів")
async def list_texts():
    texts = await get_all_texts()
    return texts


@router.get("/{text_id}", response_model=TextRead, summary="Отримати текст за id")
async def retrieve_text(text_id: int):
    text = await get_text_by_id(text_id)
    if not text:
        raise HTTPException(status_code=404, detail="Текст не знайдено.")
    return text
