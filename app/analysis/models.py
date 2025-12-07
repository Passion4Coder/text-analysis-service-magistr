from typing import Optional
from sqlalchemy import JSON, ForeignKey, DateTime, Integer, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.database import Base


from app.notes.models import NoteOrm
from app.texts.models import TextOrm


class AnalysisResultOrm(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id", ondelete="CASCADE"))
    keywords: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    embeddings: Mapped[Optional[list[float]]] = mapped_column(JSON, nullable=True)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    text: Mapped["TextOrm"] = relationship("TextOrm", back_populates="analysis_result")
    note: Mapped[Optional["NoteOrm"]] = relationship(
        "NoteOrm", back_populates="analysis_result", uselist=False
    )
