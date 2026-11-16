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

# 依赖函数:配合 FastAPI 的 Depends 使用,每个请求自动"领一个会话、用完自动还"
def get_db():
    db = SessionLocal()   # 进请求前:找工厂领一个 Session
    try:
        yield db      # 把 db 交出去给请求用(yield:请求处理期间停在这,处理完才回来)
    finally:
        db.close()    # 请求结束后打扫:无论成功还是报错,会话必关,连接还给引擎