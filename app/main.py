from fastapi import FastAPI
from app.routers import health, messages

app = FastAPI(title="good-finds-server", version="1.3.0")

app.include_router(health.router)
app.include_router(messages.router)
