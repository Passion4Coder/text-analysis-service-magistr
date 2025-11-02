from pydantic import BaseModel
from typing import Dict, Optional


class MethodBase(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict] = None


class MethodCreate(MethodBase):
    pass


class MethodRead(MethodBase):
    id: int

    class Config:
        from_attributes = True
