from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.texts.models import TextOrm
from app.analysis.models import AnalysisResultOrm
from app.analysis.keyword_extraction import extract_keywords
import time


async def process_text(
    session: AsyncSession,
    text_id: int,
    top_n: int = 10,
    diversity: float = 0.5,
) -> AnalysisResultOrm:
    start = time.time()

    result = await session.execute(select(TextOrm).where(TextOrm.id == text_id))
    text_obj: TextOrm = result.scalars().first()
    if not text_obj:
        raise ValueError(f"Текст з ідентифікатором номер {text_id} не знайдено.")

    keywords: List[Tuple[str, float]] = await extract_keywords(
        text_obj.content, top_n=top_n, diversity=diversity
    )

    analysis_result = AnalysisResultOrm(
        text_id=text_obj.id,
        keywords=[kw for kw, _ in keywords],
        lemmas=None,
        embeddings=None,
        duration_ms=int((time.time() - start) * 1000),
    )

    session.add(analysis_result)
    await session.commit()
    await session.refresh(analysis_result)

    return analysis_result
