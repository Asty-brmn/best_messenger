from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import get_db, User, Chat, Message
from schemas import ChatCreate, MessageResponse, ChatResponse
from typing import List

router = APIRouter(
    prefix="/chats",
    tags=["chats api"]
)


@router.post("", response_model=ChatResponse)
def create_chat(
    chat: ChatCreate, 
    db: Session = Depends(get_db)
):
    """Создать новый чат"""
    db_chat = Chat(name=chat.name)
    
    if chat.user_ids:
        users = (
            db.query(User)
            .filter(User.id.in_(chat.user_ids))
            .all()
        )

        if len(users) != len(chat.user_ids):
            raise HTTPException(status_code=404, detail="Some users not found")
        
        db_chat.users = users
    
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


@router.get("", response_model=List[ChatResponse])
def get_all_chats(
    chat_name: str | None = Query(None, min_length=1), 
    db: Session = Depends(get_db)
):
    """Получить все чаты"""
    db_query = db.query(Chat)
    if chat_name:
        db_query = db_query.filter(Chat.name.ilike(f"%{chat_name}%"))

    chats = db_query.all()

    if not chats:
        raise HTTPException(status_code=404, detail="Chat with this name not found")
    
    return chats

@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(
    chat_id: int, 
    db: Session = Depends(get_db)
):
    """Получить чат по ID"""
    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id)
        .first()
    )

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return chat

@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
def get_chat_messages(
    chat_id: int,  
    limit: int = Query(2, ge=1, le=100), 
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):  
    """Получить все сообщения в конкретном чате"""
    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id)
        .first()
    )

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return messages
