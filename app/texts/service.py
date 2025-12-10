from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import paginate
from app.texts.models import TextOrm


async def get_texts(session: AsyncSession, page: int, page_size: int):
    return await paginate(session, select(TextOrm).order_by(TextOrm.created_at.desc()), page, page_size)


async def get_text_by_id(session: AsyncSession, text_id: int) -> Optional[TextOrm]:
    result = await session.execute(select(TextOrm).where(TextOrm.id == text_id))

    return result.scalar_one_or_none()
