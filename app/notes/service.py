from typing import List, Optional
from sqlalchemy import select
from app.core.database import async_session_factory
from app.notes.models import NoteOrm


async def get_all_notes() -> List[NoteOrm]:
    async with async_session_factory() as session:
        result = await session.execute(
            select(NoteOrm).order_by(NoteOrm.created_at.desc())
        )
        return result.scalars().all()


async def get_note_by_id(note_id: int) -> Optional[NoteOrm]:
    async with async_session_factory() as session:
        result = await session.execute(select(NoteOrm).where(NoteOrm.id == note_id))
        return result.scalar_one_or_none()
