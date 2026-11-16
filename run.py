# run.py —— 真正的启动入口:先建表,再开机
import uvicorn

from app.config import settings
from app.database import Base, engine

if __name__ == "__main__":
    # 对照 Base 族谱上所有表定义检查数据库,缺的表自动补建(只建新表,不改已有表结构)
    Base.metadata.create_all(engine)
    # host/port/debug 全来自 settings(.env 可覆盖);reload=热重载,改代码自动重启
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)