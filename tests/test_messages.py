from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.database import Base, get_db
from app.main import app

from app.config import settings

test_engine = create_engine(
    settings.database_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
test_session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(test_engine)

def override_get_db():
    db = test_session()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_message():
    resp = client.post(
        "/api/messages",
        json={"content": "test message", "sender": "测试员"},
    )
    assert resp.status_code == 200
    assert resp.json()["sender"] == "测试员"
    assert "id" in resp.json()

def test_list_messages():
    resp = client.get("/api/messages")
    assert resp.status_code == 200
    assert any(m["content"] == "test message" for m in resp.json())