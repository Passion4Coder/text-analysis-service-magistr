from typing import Dict, List, Optional
from sqlalchemy import JSON, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.analysis.models import AnalysisResultOrm


class Model(DeclarativeBase):
    pass


class MethodOrm(Model):
    __tablename__ = "methods"  
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    parameters: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True)
    
    analysis_results: Mapped[List[AnalysisResultOrm]] = relationship(back_populates="method", cascade="all, delete")
    