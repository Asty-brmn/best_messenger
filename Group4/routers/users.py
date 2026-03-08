from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, User
from schemas import UserCreate, UserResponse
from typing import List

router = APIRouter(prefix="/users", tags=["users api"])


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя"""
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Получить всех пользователей"""
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получить пользователя по ID"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
