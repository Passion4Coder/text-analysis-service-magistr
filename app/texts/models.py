from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.database import Base


if TYPE_CHECKING:
    from app.analysis.models import AnalysisResultOrm
    from app.notes.models import NoteOrm


class TextOrm(Base):
    __tablename__ = "texts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="uk")
    source_type: Mapped[str] = mapped_column(String(50), default="upload")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    analysis_result: Mapped["AnalysisResultOrm"] = relationship(
        "AnalysisResultOrm",
        back_populates="text",
        cascade="all, delete-orphan",
        uselist=False,
    )
    notes: Mapped[List["NoteOrm"]] = relationship(
        "NoteOrm", back_populates="text", cascade="all, delete-orphan"
    )
