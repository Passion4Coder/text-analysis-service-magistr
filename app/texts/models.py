from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database import Base


if TYPE_CHECKING:
    from analysis.models import AnalysisResultOrm
    from notes.models import NoteOrm


class TextOrm(Base):
    __tablename__ = "texts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(10), default="uk")
    source_type: Mapped[str] = mapped_column(String(50), default="manual_upload")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    analysis_results: Mapped[List["AnalysisResultOrm"]] = relationship(
        "AnalysisResultOrm", back_populates="text", cascade="all, delete-orphan"
    )
    notes: Mapped[List["NoteOrm"]] = relationship(
        "NoteOrm", back_populates="text", cascade="all, delete-orphan"
    )
