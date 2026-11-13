# 第 6 课:CRUD 接口 + 依赖注入

## 目标

POST 存消息、GET 拉列表——第 5 课的表开始干活。

## 先建契约(schemas.py 追加)

```python
class MessageCreate(BaseModel):       # 收的契约:客户端发什么
    sender: str
    content: str                      # id 和时间是数据库的事,轮不到客户端给

class MessageResponse(BaseModel):     # 给的契约:返回什么
    model_config = ConfigDict(from_attributes=True)   # ← 学会"从对象属性抄字段"

    id: int
    sender: str
    content: str
    created_at: datetime
```

一进一出,各管一门。`from_attributes=True` 是转换插头:handler 返回的是 SQLAlchemy 对象(不是字典),靠它 Pydantic 才会从对象属性抄字段组装响应——**两副面孔的转换器**。

## 传送带(database.py 追加)

```python
def get_db():
    db = SessionLocal()
    try:
        yield db      # 把 db 交出去给请求用
    finally:
        db.close()    # 请求结束后打扫
```

`yield` 夹心饼干:前面准备,后面清理。**每个请求各领一个新 session,用完必还**,并发互不踩脚。

## 路由(app/routers/messages.py)

```python
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(tags=["messages"])

@router.post("/api/messages", response_model=schemas.MessageResponse)
def create_message(payload: schemas.MessageCreate, db: Session = Depends(get_db)):
    msg = models.Message(sender=payload.sender, content=payload.content)
    db.add(msg)       # 登记:准备写入
    db.commit()       # 落库:事务提交,真正写进磁盘
    db.refresh(msg)   # 回读:把数据库生成的 id、created_at 取回来
    return msg

@router.get("/api/messages", response_model=list[schemas.MessageResponse])
def list_messages(db: Session = Depends(get_db)):
    stmt = select(models.Message).order_by(models.Message.id.desc())
    return db.scalars(stmt).all()
```

main.py 老规矩收编:`app.include_router(messages.router)`。

## 灵魂概念:Depends

```python
db: Session = Depends(get_db)
```

普通参数自己传值;`Depends(...)` 是**声明**:"这个参数我不管,FastAPI 你负责"。请求进来,框架自动调 `get_db()` 塞给你,结束自动回收。**函数里只剩业务逻辑,资源开关完全交给框架**——忘关连接这类事故从根上消灭。它还有第二张牌(第 7 课):能注入,就能替换。

## 状态码是声明,不是魔法

FastAPI **默认所有接口返回 200**。想让 POST 返回 201(Created,REST 惯例),必须显式声明:

```python
@router.post("/api/messages", status_code=status.HTTP_201_CREATED, ...)
```

声明后 /docs 也会如实展示。(本项目最终选择了让测试断言 200、保持默认——两条路都通,但"创建返回 201"更标准。)

## 验收仪式(本课程最爽的一刻)

1. `python run.py`,打开 `/docs`
2. POST /api/messages → Try it out → `{"sender": "张三", "content": "..."}` → Execute
3. 响应里的 `id` 和 `created_at` **不是你写的,是数据库填的**
4. **Ctrl+C 杀掉服务,重启,再 GET——数据还在**。这就是"为什么需要数据库"的最终答案

## 踩过的坑

- 路径少了开头的 `/` → POST 全部 404,数据"消失"(其实从没进门)。响应码分诊:404 没进门 / 422 被门卫拦(校验不过)/ 500 进门摔了(代码错)

## 自测

1. add / commit / refresh 各干什么?漏掉 refresh 会怎样?
2. `Depends(get_db)` 替你干了哪两件事?
