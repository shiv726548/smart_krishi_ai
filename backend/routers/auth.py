from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
import hashlib

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class UserRegister(BaseModel):
    full_name: str
    phone_number: str
    password: str
    location: Optional[str] = "Maharashtra, India"
    preferred_language: Optional[str] = "en"

class UserLogin(BaseModel):
    phone_number: str
    password: str

def hash_pass(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.phone_number == user_data.phone_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    new_user = User(
        full_name=user_data.full_name,
        phone_number=user_data.phone_number,
        hashed_password=hash_pass(user_data.password),
        location=user_data.location,
        preferred_language=user_data.preferred_language
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "status": "success",
        "message": "Farmer account registered successfully",
        "user_id": new_user.id,
        "token": f"mock-jwt-token-user-{new_user.id}"
    }

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == credentials.phone_number).first()
    if not user or user.hashed_password != hash_pass(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid phone number or password")
    
    return {
        "status": "success",
        "message": "Login successful",
        "user_id": user.id,
        "full_name": user.full_name,
        "location": user.location,
        "preferred_language": user.preferred_language,
        "token": f"mock-jwt-token-user-{user.id}"
    }
