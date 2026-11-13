# 第 5 课:数据库(SQLite + SQLAlchemy)

## 目标

数据活过重启。为 `weixin_msg` 这样的业务存住每一条消息。

## 为什么需要数据库

| 方案 | 结局 |
|---|---|
| 变量/字典 | 断电就没,进程间不互通 |
| 文本文件 | 格式自己管,并发写入互相踩 |
| **数据库** | 增删改查、并发、索引全包 |

- **SQLite** = 数据库界的记事本:零安装,**整个库就是磁盘上一个文件**,Python 自带驱动。将来升级 MySQL/PostgreSQL 只改配置里一个字符串
- **SQLAlchemy** = 翻译官(ORM):写 Python 类,它翻译成 SQL

## 核心概念:一个"消息"有两副面孔

| 身份 | 文件 | 职责 |
|---|---|---|
| API 契约 | `schemas.py`(Pydantic) | 对外展示成什么样 |
| 表结构 | `models.py`(SQLAlchemy) | 数据库里怎么存 |

它们迟早分道扬镳:表里可能存 `password_hash`,API 响应永远不该吐密码。**这是 FastAPI 社区的固定约定,项目再小也遵守。**

## 代码

```python
# app/database.py —— 水管工程
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass
```

- `engine`:连接引擎(数据源);`check_same_thread` 是 SQLite 专属——解除单线程限制,FastAPI 多线程才能访问
- `SessionLocal`:会话工厂(第 6 课用)
- `Base`:所有表类的族长,想当表就继承它

```python
# app/models.py —— 表结构
from datetime import datetime

from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
```

句式是不是眼熟?`字段: 类型 = 附加信息`——和 Pydantic 的 `port: int = 8001` 同款。

```python
# run.py 里,点火前先把桌子摆好
from app import models  # noqa: F401 —— 关键!
Base.metadata.create_all(engine)
```

## 本课最大的坑:建表的"注册陷阱"

**表在"类被定义"那一刻注册进 `Base.metadata`,而类定义要靠 import 触发。** `from app import models` 这行看似没用,实则是触发注册——漏了它,`create_all` 会**完美地、静默地、什么表都不建**:不报错、不警告、不留痕。

真实案发:数据库文件 0 字节、"看到文件了"以为表建好了——**文件在 ≠ 表在**(`sqlite3.connect()` 会顺手创建空文件)。真正的验证方式:

```powershell
python -c "import sqlite3; con = sqlite3.connect('lianxi.db'); print(con.execute('SELECT name, type FROM sqlite_master').fetchall())"
```

看到 `('message', 'table')` 才算数。

## 自测

1. schemas.py 和 models.py 各装什么?为什么要分两个文件?
2. `create_all` 建了 0 张表,不报错,第一个该查什么?
