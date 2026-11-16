# models.py —— 表的图纸:一个类 = 数据库里的一张表
from datetime import datetime

from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Message(Base):
    __tablename__ = "message"   # 映射到数据库里的 message 表

    id: Mapped[int] = mapped_column(primary_key=True)          # 主键,整数,自动递增
    sender: Mapped[str] = mapped_column(String(50))            # 发送人,最长 50 字符
    content: Mapped[str] = mapped_column(Text)                 # 消息正文,长文本不限长度
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())  # 创建时间,插入时由数据库自动填