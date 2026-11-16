from fastapi import FastAPI

from app.schemas import testData, testDataOut

app = FastAPI(title="FastAPI Demo", description="FastAPI Demo", version="0.1.0")

@app.get("/test", response_model=testDataOut)

def test():
    data = testData(service="FastAPI Demo", version="0.1.0")
    return testDataOut(data=data)