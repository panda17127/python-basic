from pydantic import BaseModel, ConfigDict
from datetime import datetime

class testData(BaseModel):
	service: str
	version: str

class testDataOut(BaseModel):
	code: int = 200
	msg: str = "OK"
	data: testData

class MessageCreate(BaseModel):       # 收的契约:客户端发什么(POST 的请求体)
    sender: str                       # 发送人,必填,少了直接 422
    content: str                      # id 和时间是数据库的事,轮不到客户端给

class MessageResponse(BaseModel):     # 给的契约:返回什么
    # from_attributes=True:允许"从 ORM 对象属性抄字段"(db_message.id → id)
    # pydantic 默认只认字典,开了这个开关才能直接返回 SQLAlchemy 的对象
    model_config = ConfigDict(from_attributes=True)   # ← 学会"从对象属性抄字段"

    id: int                           # 数据库生成的自增主键
    sender: str
    content: str
    created_at: datetime              # 数据库 func.now() 填的创建时间