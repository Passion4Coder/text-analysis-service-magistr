from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.texts.models import TextOrm


class AnalysisResultOrm(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id", ondelete="CASCADE"))
    keywords: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    llm_model: Mapped[str] = mapped_column(String(256), nullable=False)
    embedding_model: Mapped[str] = mapped_column(String(256), nullable=False)
    text_word_count: Mapped[int] = mapped_column(Integer, nullable=False)
    n_user: Mapped[int] = mapped_column(Integer, nullable=False)
    n_semantic_recommended: Mapped[int] = mapped_column(Integer, nullable=False)
    n_final: Mapped[int] = mapped_column(Integer, nullable=False)
    use_semantic_n: Mapped[bool] = mapped_column(Boolean, nullable=False)
    diversity: Mapped[float] = mapped_column(Float, nullable=False)
    keybert_duration_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    llm_duration_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    text: Mapped["TextOrm"] = relationship("TextOrm", back_populates="analysis_result")
