from fastapi import FastAPI

from app.routers import test

app = FastAPI(title="good-finds-server", version="1.3.0")
app.include_router(test.router)     # 收编:把插线板插到主插座