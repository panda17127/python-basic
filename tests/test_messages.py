from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.database import get_db, Base
from app.main import app

# 测试专用数据库:内存 SQLite。注意冒号数量!
# "sqlite://"   = 两个冒号,纯内存,进程结束即消失
# "sqlite:///./lianxi.db" = 三个冒号 + 路径,磁盘文件(生产用那个)
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,   # 全体共用同一条连接,内存库才不会"每次连接都失忆"
)
TestSession = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

Base.metadata.create_all(test_engine)

def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db   # 核心:换水管

client = TestClient(app)   # 进程内模拟浏览器,不用启动服务器、不占端口

def test_create_message():
    resp = client.post("/api/messages", json={"sender": "测试员", "content": "pytest 第一条"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["sender"] == "测试员"
    assert "id" in data


def test_list_messages():
    resp = client.get("/api/messages")
    assert resp.status_code == 200
    assert any(m["content"] == "pytest 第一条" for m in resp.json())