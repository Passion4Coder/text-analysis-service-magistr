from typing import List, Optional
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

from app.analysis.models import AnalysisResultOrm
from app.notes.models import NoteOrm


class Model(DeclarativeBase):
    pass


class TextOrm(Model):
    __tablename__ = "texts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(10), default="uk")
    source_type: Mapped[str] = mapped_column(String(50), default="manual_upload")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    analysis_results: Mapped[List[AnalysisResultOrm]] = relationship(back_populates="text", cascade="all, delete")
    notes: Mapped[List[NoteOrm]] = relationship(back_populates="text", cascade="all, delete")