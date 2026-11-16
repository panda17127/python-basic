from fastapi import FastAPI

app = FastAPI(title="FastAPI Demo", description="FastAPI Demo", version="0.1.0")

@app.get("/test") 

def test():
    return {"code": "200", "msg": "ok", "data": {"title": "FastAPI Demo", "version": "0.1.0"}}