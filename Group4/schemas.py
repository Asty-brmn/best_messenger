from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import re


class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Имя пользователя, от 2 до 50 символов",
    )

    @validator("username")
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError(
                "Username must contain only letters, numbers and underscores"
            )
        return v


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class ChatBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Название чата, от 1 до 100 символов",
    )

    @validator("name")
    def validate_chat_name(cls, v):
        if not v.strip():
            raise ValueError("Chat name cannot be empty or contain only spaces")
        return v.strip()


class ChatCreate(ChatBase):
    user_ids: List[int] = Field(
        default=[], description="Список ID пользователей в чате"
    )

    @validator("user_ids")
    def validate_user_ids(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("Duplicate user IDs are not allowed")
        return v


class ChatResponse(ChatBase):
    id: int
    users: List[UserResponse] = []

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Текст сообщения, от 1 до 1000 символов",
    )
    author_id: int = Field(
        ..., gt=0, description="ID автора сообщения (должен быть положительным)"
    )
    chat_id: int = Field(..., gt=0, description="ID чата (должен быть положительным)")

    @validator("text")
    def validate_message_text(cls, v):
        if not v.strip():
            raise ValueError("Message text cannot be empty or contain only spaces")
        return v.strip()


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
