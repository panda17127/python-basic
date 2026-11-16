from fastapi import APIRouter
from app.schemas import testData, testDataOut

router = APIRouter(tags=["test"])

@router.get("/api/test", response_model=testDataOut)

def test():
    data = testData(service="FastAPI Demo", version="0.1.0")
    return testDataOut(data=data)