from typing import Dict, Optional
from sqlalchemy import JSON, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

from app.analysis.models import AnalysisResultOrm
from app.texts.models import TextOrm


class Model(DeclarativeBase):
    pass


class NoteOrm(Model):
    __tablename__ = "notes"  
    
    id: Mapped[int] = mapped_column(primary_key=True)
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id"), ondelete="CASCADE")
    analysis_result_id: Mapped[int] = mapped_column(ForeignKey("analysis_results.id"), ondelete="CASCADE")
    structure: Mapped[Dict] = mapped_column(JSON)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    text: Mapped[TextOrm] = relationship(back_populates="notes")
    analysis_result: Mapped[AnalysisResultOrm] = relationship(back_populates="note")
