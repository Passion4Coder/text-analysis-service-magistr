from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.analysis.models import AnalysisResultOrm
from app.stats.schemas import KeywordCountStats, StatsResponse

CHART_ROWS_LIMIT = 2_000


async def get_stats(session: AsyncSession) -> StatsResponse:
    keyword_count = await get_keyword_count_stats(session)
    diversity_performance = await get_diversity_performance_stats(session)
    analysis_duration = await get_analysis_duration_stats(session)

    return StatsResponse(
        keyword_count=keyword_count,
        diversity_performance=diversity_performance,
        analysis_duration=analysis_duration,
    )


async def get_keyword_count_stats(session: AsyncSession) -> List[KeywordCountStats]:
    result = await session.execute(
        select(
            AnalysisResultOrm.n_user,
            AnalysisResultOrm.n_semantic_recommended,
            AnalysisResultOrm.n_final,
        )
        .order_by(AnalysisResultOrm.created_at.desc())
        .limit(CHART_ROWS_LIMIT)
    )

    items = result.mappings().all()[::-1]

    return items


async def get_diversity_performance_stats(session: AsyncSession) -> List[KeywordCountStats]:
    result = await session.execute(
        select(
            AnalysisResultOrm.diversity.label("diversity"),
            func.avg(AnalysisResultOrm.keybert_duration_ms).label("avg_keybert_ms"),
            func.avg(AnalysisResultOrm.llm_duration_ms).label("avg_llm_ms"),
        )
        .group_by(AnalysisResultOrm.diversity)
        .order_by(AnalysisResultOrm.diversity)
        .limit(CHART_ROWS_LIMIT)
    )

    items = result.mappings().all()

    return items


async def get_analysis_duration_stats(session: AsyncSession) -> List[float]:
    result = await session.scalars(
        select((AnalysisResultOrm.keybert_duration_ms + AnalysisResultOrm.llm_duration_ms) / 1000)
        .order_by(AnalysisResultOrm.created_at.desc())
        .limit(CHART_ROWS_LIMIT)
    )

    items = result.all()[::-1]

    return items
