from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user_id
from app.database import get_db
from app.models import User

router = APIRouter(
prefix="/account",
tags=["Account"]
)

@router.get("/balance")
def get_balance(
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
        "user_id": user.id,
        "balance": user.balance
    }
