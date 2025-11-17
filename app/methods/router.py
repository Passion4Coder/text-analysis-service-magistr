from fastapi import APIRouter

from app.methods.schemas import MethodRead
from app.methods.service import get_all_methods_service, get_method_by_id_service


router = APIRouter(prefix="/methods", tags=["Методи ⚙️"])


@router.get(
    "/", summary="Отримати список всіх методів", response_model=list[MethodRead]
)
async def get_all_methods():
    return await get_all_methods_service()


@router.get("/{method_id}", summary="Отримати метод за id", response_model=MethodRead)
async def get_method_by_id(method_id: int):
    return await get_method_by_id_service(method_id)
