from fastapi import APIRouter

from app.config import settings
from app.schemas import testData, testDataOut

router = APIRouter(tags=["test"])

@router.get("/api/test", response_model=testDataOut)

def test():
    data = testData(service=settings.app_name, version=settings.version)
    return testDataOut(data=data)