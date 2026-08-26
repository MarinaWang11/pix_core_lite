from fastapi import FastAPI
from app.database import Base, engine
from app import models

app = FastAPI(title="PIX Core Lite")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "PIX Core API is running"}