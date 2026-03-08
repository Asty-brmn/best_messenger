from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class ChatBase(BaseModel):
    name: str


class ChatCreate(ChatBase):
    user_ids: List[int] = []


class ChatResponse(ChatBase):
    id: int
    users: List[UserResponse] = []

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    text: str
    author_id: int
    chat_id: int


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
