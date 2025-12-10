from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def paginate(session: AsyncSession, query: Select, page: int, page_size: int) -> dict:
    limit = page_size * page
    offset = (page - 1) * page_size

    count = await session.scalar(select(func.count()).select_from(query.subquery()))
    items = [item for item in await session.scalars(query.limit(limit).offset(offset))]

    return {"count": count, "items": items}
