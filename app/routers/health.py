from fastapi import APIRouter
from app.schemas import HealthData, HealthResponse

router = APIRouter(tags=["health"])

@router.get("/api/health", response_model=HealthResponse)

def health():
  return HealthResponse(data=HealthData(service="good-finds-server", version="1.3.0"))