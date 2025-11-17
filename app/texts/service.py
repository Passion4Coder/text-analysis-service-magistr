from typing import List, Optional
from sqlalchemy import select
from app.core.database import async_session_factory
from app.texts.models import TextOrm


async def get_all_texts() -> List[TextOrm]:
    async with async_session_factory() as session:
        result = await session.execute(
            select(TextOrm).order_by(TextOrm.created_at.desc())
        )
        return result.scalars().all()


async def get_text_by_id(text_id: int) -> Optional[TextOrm]:
    async with async_session_factory() as session:
        result = await session.execute(select(TextOrm).where(TextOrm.id == text_id))
        return result.scalar_one_or_none()
