from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
class LoginRequest(BaseModel):
    cpf: str
    password: str

class TransferRequest(BaseModel):
    pix_key_receiver: str
    amount: Decimal

class PixKeyRequest(BaseModel):
    key_type: str
    key_value: str