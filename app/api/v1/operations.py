from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas import OperationRequest, OperationResponse, TransferCreateShema
from app.service import operations as operations_service
from app.dependecy import get_db, get_current_user
from app.models import User

router = APIRouter()

@router.post("/operation/income", response_model=OperationResponse)
def add_income(operation: OperationRequest, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return operations_service.add_income(db, current_user, operation)

@router.post("/operation/expense", response_model=OperationResponse)
def add_expense(operation: OperationRequest, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return operations_service.add_expense(db, current_user, operation)

@router.get("/operations", response_model=list[OperationResponse])
def get_operations_list(
    wallet_id: int | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    current_user: User =  Depends(get_current_user),
    db : Session = Depends(get_db)
):
    return operations_service.get_operations_list(db, current_user, wallet_id, date_from, date_to)

@router.post("/operations/transfer", response_model=OperationResponse)
def create_fransfer(
    payload: TransferCreateShema,
    user: User =  Depends(get_current_user),
    db : Session = Depends(get_db)
):
    
    return operations_service.transfer_between_wallets(db, user.id, payload.from_wallet_id, payload.to_wallet_id, payload.amount)
