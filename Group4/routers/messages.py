from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import get_db, User, Chat, Message
from schemas import MessageCreate, MessageResponse
from typing import List


router = APIRouter(prefix="/messages", tags=["messages api"])


@router.post("", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """Создать новое сообщение"""
    author = db.query(User).filter(User.id == message.author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    chat = db.query(Chat).filter(Chat.id == message.chat_id).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    if author not in chat.users:
        raise HTTPException(status_code=403, detail="User is not a member of this chat")

    db_message = Message(
        text=message.text, author_id=message.author_id, chat_id=message.chat_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@router.get("", response_model=List[MessageResponse])
def get_all_messages(
    msg_text: str | None = Query(None, min_length=1), db: Session = Depends(get_db)
):
    """Получить все сообщения"""
    db_query = db.query(Message)

    if msg_text:
        db_query = db_query.filter(Message.text.ilike(f"%{msg_text}%"))

    messages = db_query.all()

    if not messages:
        raise HTTPException(status_code=404, detail="Message with this text not found")

    return messages


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(message_id: int, db: Session = Depends(get_db)):
    """Получить сообщение по ID"""
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")


@router.delete("/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    """Удалить сообщение по ID"""
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    db.delete(message)
    db.commit()

    return {"detail": "Message deleted successfully"}
