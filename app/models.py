# SQLAlchemy allows interaction with the database, using Python objects as SQL tables

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, String, ForeignKey, DateTime
from decimal import Decimal
from app.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users" #name of the table in the database

    id: Mapped[int] = mapped_column(primary_key=True) #as a primary key it will be incremented by the database
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2))

class PixKey(Base):
    __tablename__ = "pix_keys"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    key_type: Mapped[str] = mapped_column(String(255))
    key_value: Mapped[str] = mapped_column(String(255), unique=True)

class Transfer(Base):
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(primary_key=True)
    idempotency_key: Mapped[str] = mapped_column(String(255), unique=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


