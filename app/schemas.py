from pydantic import BaseModel

class LoginRequest(BaseModel):
    cpf: str
    password: str

LoginRequest(
    cpf="11111111111",
    password="123456"
)