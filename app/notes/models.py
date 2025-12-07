from typing import Dict, Optional, TYPE_CHECKING
from sqlalchemy import JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.database import Base


if TYPE_CHECKING:
    from app.analysis.models import AnalysisResultOrm
    from app.texts.models import TextOrm


class NoteOrm(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id", ondelete="CASCADE"))
    analysis_result_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_results.id", ondelete="CASCADE")
    )
    structured_notes: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    text: Mapped["TextOrm"] = relationship("TextOrm", back_populates="notes")
    analysis_result: Mapped["AnalysisResultOrm"] = relationship(
        "AnalysisResultOrm", back_populates="note", uselist=False
    )
