# Python 项目搭建课程(FastAPI 实战)

> 从零搭出一个标准的 FastAPI 项目:骨架 → 契约 → 路由 → 配置 → 数据库 → CRUD → 测试。
> 每一课的坑都是本课程真实踩过、当场拆解的。

## 课程地图

| 序号 | 文件 | 主题 | 你将学会 |
|------|------|------|----------|
| 01 | [01-项目骨架.md](01-项目骨架.md) | 目录结构与依赖管理 | 每个文件的职责、启动命令的语义 |
| 02 | [02-数据模型-Pydantic.md](02-数据模型-Pydantic.md) | 数据契约 | Pydantic 模型、`__init__.py` 的真相 |
| 03 | [03-路由拆分-APIRouter.md](03-路由拆分-APIRouter.md) | 路由组织 | APIRouter 插线板模式、import 语法 |
| 04 | [04-配置管理.md](04-配置管理.md) | 配置与入口 | 环境变量优先级链、`__main__` 守卫、导入串 |
| 05 | [05-数据库-SQLAlchemy.md](05-数据库-SQLAlchemy.md) | 数据持久化 | ORM、双模型拆分、建表注册陷阱 |
| 06 | [06-CRUD与依赖注入.md](06-CRUD与依赖注入.md) | 增删改查接口 | Depends、session 三步曲、状态码 |
| 07 | [07-测试-pytest.md](07-测试-pytest.md) | 自动化测试 | 测试隔离、依赖替换、读红色输出 |
| 附 | [08-排错案例集.md](08-排错案例集.md) | 11 个真实报错 | 排错方法论 |

## 项目最终结构

```
lianxi/
├── app/
│   ├── __init__.py        # 包标记
│   ├── main.py            # 应用组装(4 行)
│   ├── config.py          # 配置(pydantic-settings)
│   ├── database.py        # 数据库引擎 + 会话工厂 + get_db
│   ├── models.py          # SQLAlchemy 表模型
│   ├── schemas.py         # Pydantic API 契约
│   └── routers/           # 路由(一个业务一个文件)
│       ├── __init__.py
│       ├── health.py
│       └── messages.py
├── tests/
│   └── test_messages.py   # pytest 测试(内存库隔离)
├── course/                # 本课程笔记
├── run.py                 # 启动入口
├── .env                   # 本机配置(不进 git)
├── requirements.txt       # 依赖配方
└── lianxi.db              # SQLite 数据库文件
```

## 常用命令

```powershell
pip install -r requirements.txt   # 复现环境
python run.py                     # 启动开发服务器(读 .env 配置)
python -m pytest                  # 跑测试(注意用 -m,不用裸 pytest)
```

## 学习心法(全课程反复出现的五句话)

1. **读报错先读尾**——最后一段往往写着答案
2. **响应码是分诊台**——404 没进门 / 422 被门卫拦 / 500 进门摔了
3. **`python -m` 惯用法**——pip、pytest 都用它,指名道姓永不出错
4. **显式优于隐式**——从 `__init__.py` 到状态码,声明出来的东西才可靠
5. **改一处,跑测试**——绿色是护栏,红色三秒定位
