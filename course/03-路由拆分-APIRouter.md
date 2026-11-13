# 第 3 课:路由拆分(APIRouter)

## 目标

让 main.py 只做"组装",不做"干活"。项目长到 50 个接口也不乱。

## 为什么拆

所有接口堆在 main.py = 几千行、找不到东西、协作天天冲突。**原则:一个业务领域一个文件。**

## 核心概念:APIRouter = 迷你版 app(插线板比喻)

- `app` 是**整机**:能启动服务,自己是老大
- `router` 是**插线板**:自己不通电,上面插着一排接口,等主 app 收编

```python
# app/routers/health.py
from fastapi import APIRouter
from app.schemas import HealthData, HealthResponse

router = APIRouter(tags=["health"])   # tags = /docs 里的分组标签

@router.get("/api/health", response_model=HealthResponse)   # 注意:@router.get 不是 @app.get
def health():
    return HealthResponse(data=HealthData(service="good-finds-server", version="1.3.0"))
```

```python
# app/main.py —— 瘦身成 4 行
from fastapi import FastAPI
from app.routers import health, messages

app = FastAPI(title="good-finds-server", version="1.3.0")
app.include_router(health.router)     # 收编:把插线板插到主插座
app.include_router(messages.router)
```

**`include_router` 不写会怎样**:类定义了、路由装饰了,但没人收编——插线板没通电,访问返回 404。它是子文件路由和主服务之间的**接缝**。

以后加新业务 = 建文件 → 写 router → main.py 加一行收编。

## 顺带:`from fastapi import APIRouter` 是什么意思

```python
from fastapi import APIRouter
#    └───┘        └───┘
#    从fastapi包里  拿出APIRouter这个类
```

`fastapi` 是 pip 装的第三方库;和 `from app.schemas import HealthResponse` 语法完全相同——一个从**别人写的库**拿,一个从**自己写的文件**拿,对 Python 毫无区别。

**坑:路由路径必须以 `/` 开头**。写成 `"api/messages"`(少了开头斜杠)不报错,但访问 `/api/messages` 时 404——请求死在大门口,数据库、handler 全都没执行。(详见 [08-排错案例集](08-排错案例集.md) 案例 5)

## 自测

1. router 和 app 的区别是什么?
2. 新增一个 `orders` 业务,需要动哪几个文件、各加什么?
