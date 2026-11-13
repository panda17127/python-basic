
from datetime import datetime  
from pydantic import BaseModel, ConfigDict


class HealthData(BaseModel):
    service: str
    version: str

class HealthResponse(BaseModel):
    code: int = 0
    msg: str = "ok"
    data: HealthData

class MessageCreate(BaseModel):
    sender: str
    content: str

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)   # ← 关键,后面讲

    id: int
    sender: str
    content: str
    created_at: datetime