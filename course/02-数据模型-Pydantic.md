# 第 2 课:数据模型(Pydantic)

## 目标

给接口的输入输出定"契约",让错误在开发期爆掉,而不是流到前端。

## 为什么需要模型

裸字典(`return {"code": 0, ...}`)的问题:拼错字段名、漏字段、类型给错——Python 不报错,错误直达前端。接口一多,格式全靠人肉保证。

**Pydantic 模型 = 数据契约**。你声明字段名、类型、默认值,换来三样东西:

1. **校验**——数据不符直接报错
2. **文档**——自动出现在 `/docs` 的 Swagger 里
3. **提示**——IDE 自动补全,写错字段名划红线

## 代码(现在住在 schemas.py)

```python
from pydantic import BaseModel

class HealthData(BaseModel):
    service: str
    version: str

class HealthResponse(BaseModel):
    code: int = 0          # 读作:code 是整数,默认 0
    msg: str = "ok"
    data: HealthData       # 字段可以嵌套另一个模型
```

使用:

```python
@app.get("/api/health", response_model=HealthResponse)
def health():
    return HealthResponse(data=HealthData(service="good-finds-server", version="1.3.0"))
```

`response_model=HealthResponse` 告诉 FastAPI:这个接口的输出必须长这样。

## 深讲:`__init__.py` 为什么是空的却必须有

**比喻**:房间里坐一群人只是"一群人";挂上"市场部"的牌子,他们才是一个**部门**。`__init__.py` 就是部门牌子——告诉 Python 这个文件夹是**包(package)**,可以被 import。

**import 时发生了什么**(以 `app.main` 为例):

1. 遇到 `app/` 文件夹 → 查有没有 `__init__.py`
2. 有 → 认定常规包,进去找 `main.py` → 加载
3. (Python 3.3 前)没有 → `ModuleNotFoundError`

它的价值在**文件名约定**,不在内容,所以可以是空的。内容 = 包首次被导入时执行的代码,空 = "什么都不用做"。项目变大后可以放"转手"导入:

```python
# app/__init__.py
from app.schemas import HealthResponse   # 之后可写 from app import HealthResponse
```

**诚实补充**:Python 3.3+ 的"命名空间包"让没有它的文件夹也能被 import(可实验:改名成 `.bak` 服务照样跑)。但仍要保留,三个理由:显式优于隐式、工具兼容(pytest/mypy/打包)、命名空间包是高级场景专用。

**规则递归适用**:`app/` 下的子文件夹(如 `routers/`)想被 import,也要有自己的 `__init__.py`。

**心智模型:import 路径里的"点" = 文件系统里的"斜杠"**

```
from app.routers.health import router
#    app/  routers/  health.py 里的 router
```

## 自测

1. `response_model` 换来哪三样东西?
2. `from app.routers import health` 对应磁盘上哪个文件?
