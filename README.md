# good-finds-server

基于 FastAPI + SQLAlchemy + SQLite 的学习项目：一个消息的增查小服务。

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 创建本机配置（可选，不建则全用代码里的默认值）
#    新建 .env 文件，内容示例：
#    PORT=8008
#    DEBUG=true

# 3. 启动（推荐：先自动建表，再启动服务，host/port/debug 全读配置）
python run.py
```

启动后：

- 服务地址：<http://127.0.0.1:8008>（端口以 .env 里的 `PORT` 为准，默认 8001）
- 接口文档：<http://127.0.0.1:8008/docs>（FastAPI 自动生成，可直接调试）
- 热重载：`DEBUG=true` 时开启，改代码自动重启

> 备用启动方式：`python -m uvicorn app.main:app --reload`（注意：这种方式不会自动建表，端口也不会读 .env）

## 配置说明

配置来自 `app/config.py`，取值优先级：**环境变量 > .env 文件 > 代码默认值**

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `APP_NAME` | good-finds-server | 服务名，出现在 /docs 标题和 /api/test 返回里 |
| `VERSION` | 1.3.1 | 版本号 |
| `HOST` | 127.0.0.1 | 监听地址，127.0.0.1 = 只允许本机访问 |
| `PORT` | 8001 | 监听端口 |
| `DEBUG` | true | 调试模式，true 时开热重载 |
| `DATABASE_URL` | sqlite:///./message.db | 数据库连接串 |

## 接口列表

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/test` | 测试接口，返回服务名和版本 |
| GET | `/api/messages` | 消息列表，按 id 倒序（最新在前） |
| POST | `/api/messages` | 发一条新消息 |

**发消息示例**

```bash
curl -X POST http://127.0.0.1:8008/api/messages ^
  -H "Content-Type: application/json" ^
  -d "{\"sender\": \"gao\", \"content\": \"hello\"}"
```

返回（id 自增、created_at 由数据库自动填）：

```json
{"id": 1, "sender": "gao", "content": "hello", "created_at": "2026-11-16T06:34:03"}
```

## 测试

```bash
python -m pytest tests -v
```

测试通过 `dependency_overrides` 把 `get_db` 换成测试引擎的会话、用 TestClient 直接调用应用（不需要先启动服务、不占端口）。

## 项目结构

```
python-basic/
├── run.py               # 启动入口：先建表，再启动 uvicorn
├── requirements.txt     # 依赖清单
├── .env                 # 本机配置（已被 .gitignore 排除，不入库）
├── tests/
│   └── test_messages.py # 接口测试：pytest + TestClient
└── app/
    ├── main.py          # 主插座：创建 FastAPI 实例，挂载各模块路由
    ├── config.py        # 设置中心：pydantic-settings 读 .env
    ├── database.py      # 总机房：引擎、会话工厂、Base、get_db
    ├── models.py        # 表的图纸：message 表定义
    ├── schemas.py       # 契约：请求体 / 响应体模型
    └── routers/
        ├── test.py      # /api/test
        └── messages.py  # /api/messages 查询与创建
```

## 一次请求的完整链路（以发消息为例）

```
POST /api/messages
  → schemas.MessageCreate 校验请求体（缺字段直接 422）
  → Depends(get_db) 领一个数据库会话
  → db.add / db.commit 写入 message 表
  → db.refresh 回读数据库生成的 id、created_at
  → response_model 把 ORM 对象转成 MessageResponse 的 JSON 返回
  → 请求结束，get_db 的 finally 关会话
```

## 技术栈

- [FastAPI](https://fastapi.tiangolo.com/) — Web 框架
- SQLAlchemy 2.0 — ORM（声明式模型 + Mapped 注解）
- pydantic-settings — 配置管理
- SQLite — 数据库（文件在项目根 `message.db`，已 gitignore）
- pytest — 测试（配合 fastapi.testclient 的 TestClient）
