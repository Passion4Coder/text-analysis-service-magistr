from sqlalchemy import select
from fastapi import HTTPException

from app.core.database import async_session_factory
# from app.methods.models import MethodOrm


async def get_all_methods_service():
    """Повертає всі методи."""
    # async with async_session_factory() as session:
        # result = await session.execute(select(MethodOrm))
        # return result.scalars().all()


async def get_method_by_id_service(method_id: int):
    """Повертає метод за ID або 404."""
    # async with async_session_factory() as session:
    #     result = await session.execute(
    #         select(MethodOrm).where(MethodOrm.id == method_id)
    #     )
    #     method = result.scalar_one_or_none()

    #     if method is None:
    #         raise HTTPException(status_code=404, detail="Метод не знайдено.")

    #     return method
