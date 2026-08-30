from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import Base, engine
from app.routers import auth, users, pix

app = FastAPI(title="PIX Core Lite")
security = HTTPBearer() #sender with token

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(pix.router)


@app.get("/")
def root():
    return {"message": "PIX Core API is running"}







