from fastapi import APIRouter

router = APIRouter(tags=["messages"])

@router.get("/api/messages")

def messages():

    return {"code": 200, "msg": "OK", "data": []}
