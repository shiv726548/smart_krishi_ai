from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.security import (
    TOKEN_TTL_SECONDS,
    create_access_token,
    hash_password,
    is_legacy_password_hash,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class UserRegister(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    phone_number: str = Field(min_length=7, max_length=20)
    password: str = Field(min_length=8, max_length=128)
    location: str = Field(default="", max_length=160)
    preferred_language: str = Field(default="en", pattern="^(en|hi|mr)$")

class UserLogin(BaseModel):
    phone_number: str = Field(min_length=7, max_length=20)
    password: str = Field(min_length=1, max_length=128)

@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.phone_number == user_data.phone_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    new_user = User(
        full_name=user_data.full_name,
        phone_number=user_data.phone_number,
        hashed_password=hash_password(user_data.password),
        location=user_data.location,
        preferred_language=user_data.preferred_language
    )
    db.add(new_user)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to create farmer account")
    db.refresh(new_user)
    return {
        "status": "success",
        "message": "Farmer account registered successfully",
        "user_id": new_user.id,
        "token": create_access_token(new_user.id),
        "token_type": "bearer",
        "expires_in": TOKEN_TTL_SECONDS,
    }

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == credentials.phone_number).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid phone number or password")
    if is_legacy_password_hash(user.hashed_password):
        user.hashed_password = hash_password(credentials.password)
        db.commit()

    return {
        "status": "success",
        "message": "Login successful",
        "user_id": user.id,
        "full_name": user.full_name,
        "location": user.location,
        "preferred_language": user.preferred_language,
        "token": create_access_token(user.id),
        "token_type": "bearer",
        "expires_in": TOKEN_TTL_SECONDS,
    }
