from sqlalchemy import select, text

from app.analysis.models import AnalysisResultOrm
from app.core.database import async_session_factory
from app.texts.models import TextOrm


async def clear_database():
    async with async_session_factory() as session:
        tables = [TextOrm, AnalysisResultOrm]
        for table in tables:
            result = await session.execute(select(table).limit(1))
            if result.scalar() is not None:
                break
        else:
            return {"status": "ok", "message": "База даних вже порожня."}

        for table in reversed(tables):
            await session.execute(text(f"DELETE FROM {table.__tablename__}"))
        await session.commit()

    return {"status": "ok", "message": "Базу даних очищено."}
