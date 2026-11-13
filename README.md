# lianxi

最小 FastAPI 练习项目。

## 启动

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## 接口

- `GET /api/health` — 健康检查,返回 `{"code": 0, "msg": "ok", "data": {...}}`
- `GET /docs` — 自动生成的 Swagger 文档
