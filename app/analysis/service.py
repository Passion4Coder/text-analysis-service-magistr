from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.analysis.summary_generator import (
    generate_summary_with_keywords,
    generate_text_embedding,
    generate_sentence_embeddings,
)
from app.notes.models import NoteOrm
from app.texts.models import TextOrm
from app.analysis.models import AnalysisResultOrm
from app.analysis.keyword_extraction import extract_keywords
from app.core.config import settings
from .semantic_utils import determine_top_n_semantic
import time


async def process_text(
    session: AsyncSession,
    text_id: int,
    top_n: int = 10,
    diversity: float = 0.5,
    use_semantic_n: bool = False,
) -> AnalysisResultOrm:
    analysis_result = await session.execute(select(AnalysisResultOrm).where(AnalysisResultOrm.text_id == text_id))
    analysis_entity = analysis_result.scalars().first()

    if analysis_entity:
        return analysis_entity

    start_time = time.time()

    text_result = await session.execute(select(TextOrm).where(TextOrm.id == text_id))
    text_entity = text_result.scalars().first()

    if not text_entity:
        raise ValueError(f"Текст з ідентифікатором номер {text_id} не знайдено.")

    sentence_embeddings = await generate_sentence_embeddings(text_entity.content)
    embedding_vector = await generate_text_embedding(text_entity.content)

    N_recommended = determine_top_n_semantic(sentence_embeddings)

    if use_semantic_n:
        final_n = N_recommended
    else:
        final_n = top_n

    keywords: List[Tuple[str, float]] = await extract_keywords(text_entity.content, top_n=final_n, diversity=diversity)
    keywords_only = [kw for kw, _ in keywords]
    keybert_duration_ms = int((time.time() - start_time) * 1000)

    llm_start_time = time.time()
    summary_text = await generate_summary_with_keywords(keywords_only)
    llm_duration_ms = int((time.time() - llm_start_time) * 1000)

    analysis_result = AnalysisResultOrm(
        text_id=text_entity.id,
        keywords=keywords_only,
        embeddings=embedding_vector if embedding_vector else None,
        summary_text=summary_text,
        duration_ms=keybert_duration_ms,
    )

    session.add(analysis_result)
    await session.flush()

    structured_notes = {
        "llm_model": settings.LLM_SUMMARY_MODEL,
        "key_concepts_count": len(keywords),
        "keybert_duration_ms": keybert_duration_ms,
        "embedding_model": settings.EMBEDDING_MODEL,
        "embedding_vector_dim": len(embedding_vector) if embedding_vector else 0,
        "llm_duration_ms": llm_duration_ms,
        "n_user": top_n,
        "n_semantic_recommended": N_recommended,
        "n_final": final_n,
    }

    note = NoteOrm(
        text_id=text_entity.id,
        analysis_result_id=analysis_result.id,
        structured_notes=structured_notes,
    )

    session.add(note)

    await session.commit()
    await session.refresh(analysis_result)

    return analysis_result
