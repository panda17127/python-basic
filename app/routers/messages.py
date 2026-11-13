from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models,schemas
from app.database import get_db

router = APIRouter(tags=["messages"])

@router.post("/api/messages", response_model=schemas.MessageResponse)
def create_message(payload: schemas.MessageCreate, db: Session = Depends(get_db)):
   msg = models.Message(sender=payload.sender, content=payload.content)
   db.add(msg)
   db.commit()
   db.refresh(msg)
   return msg

@router.get("/api/messages", response_model=list[schemas.MessageResponse])
def list_messages(db: Session = Depends(get_db)):
  stmt = select(models.Message).order_by(models.Message.id.desc())
  return db.scalars(stmt).all()