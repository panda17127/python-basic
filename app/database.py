# database.py —— 数据库"总机房":全项目共用一个引擎和一个会话工厂
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

# 引擎 = 连接总闸:管所有与数据库的底层连接,全项目只造这一个
# check_same_thread=False:SQLite 默认只许"建连接的那个线程"用它,关掉才能让 FastAPI 的多线程共享
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})

# 会话工厂:每个请求找它领一个 Session 谈事情(增删改查),用完关掉
# autocommit=False:不自动提交,改动要自己调 commit(),事务自己控制
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 模型基类(族谱起点):models.py 里的表都继承它,SQLAlchemy 靠它收集"项目里有哪些表"
class Base(DeclarativeBase):
    pass