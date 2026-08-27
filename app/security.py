from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from jose import jwt, JWTError

SECRET_KEY = "chave-secreta"
ALGORITHM = "HS256" #simetric key (sign and verify)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    ) 

    data = {
        "sub": str(user_id),
        "exp": expire
    }

    encoded_jwt = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        ) #checks signature and exp

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return int(user_id)

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )