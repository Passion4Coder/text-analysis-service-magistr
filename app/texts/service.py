from typing import Optional

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import paginate
from app.texts.models import TextOrm


async def get_texts(session: AsyncSession, page: int, page_size: int):
    return await paginate(
        session,
        select(
            TextOrm.id,
            case(
                (func.length(TextOrm.content) > 128, func.left(TextOrm.content, 128) + "..."),
                else_=TextOrm.content,
            ).label("content"),
            TextOrm.created_at,
        ).order_by(TextOrm.created_at.desc()),
        page,
        page_size,
    )


async def get_text_by_id(session: AsyncSession, text_id: int) -> Optional[TextOrm]:
    result = await session.execute(select(TextOrm).where(TextOrm.id == text_id))

    return result.scalar_one_or_none()
