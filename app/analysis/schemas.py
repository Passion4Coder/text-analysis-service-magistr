from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional

class AnalysisResultCreate(BaseModel):
    text_id: int
    method: str
    result: Any
    
    
class AnalysisResultRead(BaseModel):
    id: int
    text_id: int
    method: str
    result: dict
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class AnalysisResultUpdate(BaseModel):
    method: Optional[str] = None
    result: Optional[Any] = None      