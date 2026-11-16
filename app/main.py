from fastapi import FastAPI

from app.routers import test
from app.config import settings

app = FastAPI(title=settings.app_name, version=settings.version)
app.include_router(test.router)     # 收编:把插线板插到主插座