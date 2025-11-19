from fastapi import APIRouter
from .service import StatsService
from .schemas import GraphsResponse

router = APIRouter(prefix="/stats", tags=["Графіки 📊"])


@router.get(
    "/graphs",
    response_model=GraphsResponse,
    summary="Отримати дані для графіків метрик",
)
async def get_graphs():
    return await StatsService.get_graphs_data()
