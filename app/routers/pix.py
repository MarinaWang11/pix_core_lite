from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PixKey, User, Transfer
from app.schemas import PixKeyRequest, TransferRequest
from app.dependencies import get_current_user_id


router = APIRouter(
    prefix="/pix",
    tags=["PIX"]
)


@router.post("/keys")
def create_pix_key(
    data: PixKeyRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    existing_key = db.query(PixKey).filter(PixKey.key_value == data.key_value).first()

    if existing_key is not None:
        raise HTTPException(
            status_code=400,
            detail="PIX key already registered"
        )

    pix_key = PixKey(
        user_id=user_id,
        key_type=data.key_type,
        key_value=data.key_value
    )

    db.add(pix_key)
    db.commit()
    db.refresh(pix_key)

    return {
        "id": pix_key.id,
        "user_id": pix_key.user_id,
        "key_type": pix_key.key_type,
        "key_value": pix_key.key_value
    }


@router.post("/transfer")
def create_transfer(
    data: TransferRequest,
    x_idempotency_key: str = Header(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    existing_transfer = db.query(Transfer).filter(Transfer.idempotency_key == x_idempotency_key).first()


    if existing_transfer is not None:
        return {
            "message": "Transfer already processed",
            "transfer_id": existing_transfer.id,
            "sender_id": existing_transfer.sender_id,
            "receiver_id": existing_transfer.receiver_id,
            "amount": existing_transfer.amount
        }

    sender = db.query(User).filter(User.id == user_id).first()

    if sender is None:
        raise HTTPException(
            status_code=404,
            detail="Sender not found"
        )

    pix_key = db.query(PixKey).filter(PixKey.key_value == data.pix_key_receiver).first()

    if pix_key is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver PIX key not found"
        )

    receiver = db.query(User).filter(User.id == pix_key.user_id).first()

    if receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver not found"
        )

    if sender.id == receiver.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot transfer to yourself"
        )

    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero"
        )

    if sender.balance < data.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    try:
        sender.balance -= data.amount
        receiver.balance += data.amount

        transfer = Transfer(
            idempotency_key=x_idempotency_key,
            sender_id=sender.id,
            receiver_id=receiver.id,
            amount=data.amount
        )

        db.add(transfer)

        db.commit()

        db.refresh(transfer) #updates database

    except Exception:
        db.rollback() #undo changes
        
        raise

    return {
        "message": "Transfer successful",
        "transfer_id": transfer.id,
        "sender_id": transfer.sender_id,
        "receiver_id": transfer.receiver_id,
        "amount": transfer.amount
    }


@router.get("/transfers")
def get_transfers(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    transfers = db.query(Transfer).filter((Transfer.sender_id == user_id) |
        (Transfer.receiver_id == user_id)).all()

    return transfers