from pydantic import BaseModel
from datetime import datetime

class TextCreate(BaseModel):
    title: str
    content: str
    

class TextRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    
    class Config:
        orm_mode = True