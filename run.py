import uvicorn

from app import models  # noqa: F401 —— 导入触发表注册
from app.config import settings
from app.database import Base, engine

if __name__ == "__main__":
  Base.metadata.create_all(engine)   # 按注册的表结构,在库里建表
  uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)