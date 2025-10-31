from sqlalchemy import JSON, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Model(DeclarativeBase):
    pass

class AnalysisResultOrm(Model):
    __tablename__ = "analysis_results"  
    
    id: Mapped[int] = mapped_column(primary_key=True)
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id"))
    method: Mapped[str] = mapped_column(String(50))
    result: Mapped[str] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    