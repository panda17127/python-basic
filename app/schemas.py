from pydantic import BaseModel

class testData(BaseModel):
	service: str
	version: str

class testDataOut(BaseModel):
	code: int = 200
	msg: str = "OK"
	data: testData