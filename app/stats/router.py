from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.stats.schemas import StatsResponse
from app.stats.service import get_stats

router = APIRouter(prefix="/stats", tags=["Графіки 📊"])


@router.get("", response_model=StatsResponse, summary="Отримати дані для графіків")
async def get(session: AsyncSession = Depends(get_session)):
    return await get_stats(session)
