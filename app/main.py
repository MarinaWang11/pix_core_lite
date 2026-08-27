from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import Base, engine, get_db
from app.schemas import LoginRequest
from app.models import User
from app.security import create_access_token, verify_token
import bcrypt

app = FastAPI(title="PIX Core Lite")
security = HTTPBearer() #sender with token

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "PIX Core API is running"}

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security) #auth info
):
    token = credentials.credentials
    return verify_token(token)

@app.post("/auth/login")
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

@app.get("/me")
def me(
    user_id: int = Depends(get_current_user_id),
    db = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "cpf": user.cpf,
        "balance": user.balance
    }