# 第 7 课:测试(pytest)

## 目标

把"改代码怕弄坏"变成"改完跑一下,三秒知道好坏"。

## 为什么

项目有真实数据后,每次改代码都是一次冒险。测试 = 把"手动点一遍每个接口"写成代码,一条命令跑完。绿色 = 没弄坏;红色 = 立刻知道弄坏了什么、在哪。

## Depends 的第二张牌:能注入,就能替换

测试最大的问题:**绝不能污染真实数据库**。因为我们用了依赖注入(第 6 课),测试时可以用 `dependency_overrides` 把"真水管"换成"测试水管"——内存里的临时 SQLite:

```python
# tests/test_messages.py(完整)
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401 —— 导入触发表注册
from app.database import Base, get_db
from app.main import app

# 内存库。注意冒号数量:两个冒号=纯内存,三个+路径=磁盘文件
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

client = TestClient(app)   # 进程内模拟浏览器,不启动服务器、不占端口

def test_create_message():
    resp = client.post("/api/messages", json={"sender": "测试员", "content": "pytest 第一条"})
    assert resp.status_code == 200
    assert resp.json()["sender"] == "测试员"
    assert "id" in resp.json()

def test_list_messages():
    resp = client.get("/api/messages")
    assert resp.status_code == 200
    assert any(m["content"] == "pytest 第一条" for m in resp.json())
```

## 逐个新面孔

- **`assert` 断言**:条件真,无事发生;假,测试报红并列出期望值与实际值
- **`TestClient(app)`**:不发真网络请求,进程内直接调 FastAPI——快
- **`json={"sender": ...}`**:等于 /docs 里点 Execute

## 本课的坑:内存库的"失忆症"

`sqlite://`(两个冒号)是内存库,它有个阴险特性:**库住在"一条连接"里,连接一关,库就蒸发**。默认连接池每次拿新连接 → `create_all` 用连接 A 建的表随 A 关闭而消失 → 请求拿到连接 B,一间空房 → `no such table`。修复 = `poolclass=StaticPool`,全楼共用一条连接。

## 运行方式(注意)

```powershell
python -m pytest      # ✅ 永远用这个
pytest                # ❌ 会报"无法识别"——PATH 里没有 Scripts 目录
```

`python -m` 惯用法第二次救场(第一次是 pip):保证用的是当前 Python 的 pytest。

## 位置约定

`tests/` 放项目根目录(**不放 app/ 里**——测试不属于应用代码,打包不带它们)。pytest 靠命名发现文件(`test_*.py`)和函数(`test_*`),**不需要 `__init__.py`**。

## 红色输出的价值(测试课的灵魂)

故意把断言改错,看 pytest 的报告:

```
assert 200 == 201
 +  where 200 = <Response [200 OK]>.status_code
```

期望值、实际值、出错行号,一清二楚。**测试的价值不在绿色,在于红色时你能三秒定位。** 读完改回,再跑绿。

## 验证隔离

跑完测试查真实库:行数应该不变(pytest 的数据没漏进来):

```powershell
python -c "import sqlite3; print(sqlite3.connect('lianxi.db').execute('SELECT COUNT(*) FROM message').fetchone())"
```

## 自测

1. 测试为什么不会污染真实数据库?靠哪两个机制?
2. StaticPool 解决什么问题?不加会报什么错?
