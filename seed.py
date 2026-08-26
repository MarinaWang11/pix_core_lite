from app.models import User
from app.database import SessionLocal
import bcrypt

def hash_password(password: str) -> str:
    password_bytes = bcrypt.hashpw(password.encode("utf-8") , bcrypt.gensalt())
    hash_password = str(password_bytes.decode())

    return hash_password

user0 = User(
    cpf="11111111111",
    hashed_password=hash_password("123456"),
    balance=1000.00,
)

user1 = User(
    cpf="22222222222",
    hashed_password=hash_password("555"),
    balance=2500.05,
)

db = SessionLocal() #creates session

try:
    db.add(user0)
    db.add(user1)

    db.commit()
finally:
    db.close()


