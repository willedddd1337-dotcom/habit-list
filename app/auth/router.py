from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import UserOrm
from app.auth.utils import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterSchema(BaseModel):
    username: str
    password: str
    email: str

class LoginSchema(BaseModel):
    username: str
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenSchema)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    # проверяем что username не занят
    existing = db.query(UserOrm).filter(UserOrm.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Имя пользователя уже занято")

    # создаём пользователя
    user = UserOrm(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # сразу возвращаем токен
    token = create_token(user.id)
    return TokenSchema(access_token=token)

@router.post("/login", response_model=TokenSchema)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    # ищем пользователя
    user = db.query(UserOrm).filter(UserOrm.username == data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # проверяем пароль
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = create_token(user.id)
    return TokenSchema(access_token=token)