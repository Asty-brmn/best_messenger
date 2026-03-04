from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from database import init_db, get_db, User, Chat, Message
from schemas import (
    UserCreate, UserResponse,
    ChatCreate, ChatResponse,
    MessageCreate, MessageResponse
)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {"message": "Yra, pobeda!"}

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя"""
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Получить всех пользователей"""
    return db.query(User).all()


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получить пользователя по ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/chats", response_model=ChatResponse)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    """Создать новый чат"""
    db_chat = Chat(name=chat.name)
    
    if chat.user_ids:
        users = db.query(User).filter(User.id.in_(chat.user_ids)).all()
        if len(users) != len(chat.user_ids):
            raise HTTPException(status_code=404, detail="Some users not found")
        db_chat.users = users
    
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


@app.get("/chats", response_model=List[ChatResponse])
def get_all_chats(
    chat_name: str | None = Query(None, min_length=1), 
    db: Session = Depends(get_db)
):
    """Получить все чаты"""
    if chat_name is None:
        return db.query(Chat).all()
    
    chats = (
        db.query(Chat)
        .filter(Chat.name.ilike(f"%{chat_name}%"))
        .all()
    )

    if not chats:
        raise HTTPException(status_code=404, detail="Chat with this name not found")
    
    return chats



@app.get("/chats/{chat_id}", response_model=ChatResponse)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    """Получить чат по ID"""
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@app.post("/messages", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """Создать новое сообщение"""
    author = db.query(User).filter(User.id == message.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    chat = db.query(Chat).filter(Chat.id == message.chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    if author not in chat.users:
        raise HTTPException(
            status_code=403, 
            detail="User is not a member of this chat"
        )
    
    db_message = Message(
        text=message.text,
        author_id=message.author_id,
        chat_id=message.chat_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@app.get("/messages", response_model=List[MessageResponse])
def get_all_messages(db: Session = Depends(get_db)):
    """Получить все сообщения"""
    return db.query(Message).all()


@app.get("/messages/{message_id}", response_model=MessageResponse)
def get_message(message_id: int, db: Session = Depends(get_db)):
    """Получить сообщение по ID"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@app.get("/chats/{chat_id}/messages", response_model=List[MessageResponse])
def get_chat_messages(
    chat_id: int,  
    limit: int = Query(2, ge=1, le=100), 
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):  
    """Получить все сообщения в конкретном чате"""
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at)
        .offset(offset)
        .limit(limit)
        .all()
    )
