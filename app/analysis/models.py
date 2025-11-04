from typing import Dict, Optional, TYPE_CHECKING
from sqlalchemy import JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database import Base


if TYPE_CHECKING:
    from methods.models import MethodOrm
    from notes.models import NoteOrm
    from texts.models import TextOrm


class AnalysisResultOrm(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id", ondelete="CASCADE"))
    method_id: Mapped[int] = mapped_column(ForeignKey("methods.id", ondelete="CASCADE"))
    keywords: Mapped[list[str]] = mapped_column(JSON)
    definitions: Mapped[list[Dict[str, str]]] = mapped_column(JSON)
    metrics: Mapped[Optional[Dict[str, float]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    text: Mapped["TextOrm"] = relationship("TextOrm", back_populates="analysis_results")
    method: Mapped["MethodOrm"] = relationship(
        "MethodOrm", back_populates="analysis_results"
    )
    note: Mapped[Optional["NoteOrm"]] = relationship(
        "NoteOrm", back_populates="analysis_result", uselist=False
    )
