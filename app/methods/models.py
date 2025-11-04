from typing import Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


if TYPE_CHECKING:
    from analysis.models import AnalysisResultOrm


class MethodOrm(Base):
    __tablename__ = "methods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    parameters: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True)

    analysis_results: Mapped[List["AnalysisResultOrm"]] = relationship(
        "AnalysisResultOrm", back_populates="method", cascade="all, delete-orphan"
    )
