# messages.py —— 消息模块:查消息列表 + 发新消息
from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db

router = APIRouter(tags=["messages"])   # tags 只影响 /docs 里的分组标题

# ---------- 查:GET /api/messages,返回按 id 倒序的消息列表 ----------
@router.get("/api/messages", response_model=list[schemas.MessageResponse])

def list_messages(db: Session = Depends(get_db)):
    # Depends(get_db):进请求前自动领会话,请求结束自动还(见 database.get_db)
    # order_by(id desc):id 倒序 = 最新发的排最前
    stms = select(models.Message).order_by(models.Message.id.desc())
    return db.scalars(stms).all()   # scalars:拿 ORM 对象本身(不是元组);all():装成列表

# ---------- 增:POST /api/messages,发一条新消息 ----------
@router.post("/api/messages", response_model=schemas.MessageResponse)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    # message:请求体已按 MessageCreate 自动校验,走到这里字段一定齐全
    db_message = models.Message(content=message.content, sender=message.sender)
    db.add(db_message)      # 登记进会话:此刻还没写库
    db.commit()             # 真正写库,id 和 created_at 由数据库生成
    db.refresh(db_message)  # 回读:把数据库生成的 id/created_at 抄回对象,不刷就是空
    return db_message       # response_model 自动把 ORM 对象转成 MessageResponse 的 JSON