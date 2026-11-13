from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# engine = 与数据库的连接引擎(数据源)
# SessionLocal = 会话工厂(以后读写数据的“工作事务”，下节课用)
# Base = 所有表类的“族长”，谁想当表，继承它
# check_same_thread 是 SQLite 专属参数：FastAPI 多线程访问它，得解除“单线程”默认限制
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()