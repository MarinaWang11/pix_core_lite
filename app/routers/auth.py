from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import bcrypt

from app.database import get_db
from app.models import User
from app.schemas import LoginRequest
from app.security import create_access_token


router = APIRouter(
    tags=["Auth"]
)

@router.post("/auth/login")
def login(
    data: LoginRequest,
    db = Depends(get_db) #session
):
    user = db.query(User).filter(User.cpf == data.cpf).first()

    if user is None:
        return{"error": "Invalid credentials"}

    
    #looks stored hash, identifies salt and checks if A reproduces B
    if(bcrypt.checkpw(data.password.encode("utf-8"), user.hashed_password.encode("utf-8"))):
        token = create_access_token(user.id)

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    return {"error": "Invalid credentials"}