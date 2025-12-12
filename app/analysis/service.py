import time
from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.analysis.keyword_extraction import extract_keywords
from app.analysis.models import AnalysisResultOrm
from app.analysis.summary_generator import (
    generate_sentence_embeddings,
    generate_summary_with_keywords,
    llm_keyword_refinement,
)
from app.core.config import settings
from app.texts.models import TextOrm
from app.texts.service import get_text_by_id

from app.analysis.semantic_utils import determine_top_n_semantic


async def process_text(
    session: AsyncSession,
    text_id: int,
    top_n: int,
    diversity: float,
    use_semantic_n: bool = False,
) -> AnalysisResultOrm:
    analysis_entity: Optional[
        AnalysisResultOrm
    ] = await get_analysis_result_by_text_id_and_params(
        session, text_id, top_n, diversity, use_semantic_n
    )

    if analysis_entity:
        return analysis_entity

    text_entity: Optional[TextOrm] = await get_text_by_id(session, text_id)

    if not text_entity:
        raise ValueError(f"Текст з ідентифікатором {text_id} не знайдено.")

    start_time = time.time()

    sentence_embeddings = await generate_sentence_embeddings(text_entity.content)
    N_recommended = determine_top_n_semantic(sentence_embeddings)

    if use_semantic_n:
        final_n = N_recommended
    else:
        final_n = top_n

    keywords: List[Tuple[str, float]] = await extract_keywords(
        text_entity.content, top_n=final_n, diversity=diversity
    )
    keywords_only = [kw for kw, _ in keywords]
    keybert_duration_ms = int((time.time() - start_time) * 1000)

    text_word_count = len(text_entity.content.split())

    validated_keywords = await llm_keyword_refinement(
        title=text_entity.title,
        initial_keywords=keywords_only,
        final_n=final_n,
    )

    llm_start_time = time.time()
    summary_text = await generate_summary_with_keywords(
        title=text_entity.title,
        keywords=validated_keywords,
        text_word_count=text_word_count,
    )
    llm_duration_ms = int((time.time() - llm_start_time) * 1000)

    analysis_result = AnalysisResultOrm(
        text_id=text_entity.id,
        keywords=validated_keywords,
        summary_text=summary_text,
        llm_model=settings.LLM_SUMMARY_MODEL,
        embedding_model=settings.EMBEDDING_MODEL,
        text_word_count=text_word_count,
        n_user=top_n,
        n_semantic_recommended=N_recommended,
        n_final=len(validated_keywords),
        use_semantic_n=use_semantic_n,
        diversity=diversity,
        keybert_duration_ms=keybert_duration_ms,
        llm_duration_ms=llm_duration_ms,
    )

    session.add(analysis_result)
    await session.commit()

    return analysis_result


async def get_analysis_result_by_text_id_and_params(
    session: AsyncSession,
    text_id: int,
    top_n: int,
    diversity: float,
    use_semantic_n: bool,
) -> Optional[AnalysisResultOrm]:
    filters = [
        AnalysisResultOrm.text_id == text_id,
        AnalysisResultOrm.use_semantic_n == use_semantic_n,
        AnalysisResultOrm.diversity == diversity,
    ]

    if not use_semantic_n:
        filters.append(AnalysisResultOrm.n_user == top_n)

    result = await session.execute(select(AnalysisResultOrm).where(*filters))

    return result.scalars().first()
