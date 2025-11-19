from sqlalchemy import select, func
from app.core.database import async_session_factory
from app.analysis.models import AnalysisResultOrm
from app.methods.models import MethodOrm


class StatsService:
    @staticmethod
    async def get_graphs_data():
        async with async_session_factory() as session:
            stmt = (
                select(
                    MethodOrm.name,
                    func.avg(AnalysisResultOrm.metrics["precision"].as_float()).label(
                        "precision"
                    ),
                    func.avg(AnalysisResultOrm.metrics["recall"].as_float()).label(
                        "recall"
                    ),
                )
                .join(AnalysisResultOrm, AnalysisResultOrm.method_id == MethodOrm.id)
                .group_by(MethodOrm.name)
            )

            result = await session.execute(stmt)
            metrics = []
            for row in result.all():
                precision = row.precision
                recall = row.recall
                f1_score = (
                    2 * precision * recall / (precision + recall)
                    if (precision + recall) > 0
                    else 0
                )
                metrics.append(
                    {
                        "method_name": row.name,
                        "precision": precision,
                        "recall": recall,
                        "f1_score": f1_score,
                    }
                )

            precision_comparison = metrics
            recall_comparison = metrics
            f1_comparison = metrics

            date_trunc_day = func.date_trunc("day", AnalysisResultOrm.created_at).label(
                "date"
            )

            stmt_time = (
                select(
                    date_trunc_day,
                    MethodOrm.name,
                    func.avg(AnalysisResultOrm.metrics["precision"].as_float()).label(
                        "avg_precision"
                    ),
                    func.avg(AnalysisResultOrm.metrics["recall"].as_float()).label(
                        "avg_recall"
                    ),
                )
                .join(MethodOrm, AnalysisResultOrm.method_id == MethodOrm.id)
                .group_by(date_trunc_day, MethodOrm.name)
                .order_by(date_trunc_day)
            )

            result_time = await session.execute(stmt_time)
            f1_over_time = [
                {
                    "date": row.date.isoformat(),
                    "method_name": row.name,
                    "f1_score": (
                        2
                        * row.avg_precision
                        * row.avg_recall
                        / (row.avg_precision + row.avg_recall)
                        if (row.avg_precision + row.avg_recall) > 0
                        else 0
                    ),
                }
                for row in result_time.all()
            ]

            return {
                "precision_comparison": precision_comparison,
                "recall_comparison": recall_comparison,
                "f1_comparison": f1_comparison,
                "f1_over_time": f1_over_time,
            }
