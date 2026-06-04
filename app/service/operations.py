from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas import OperationRequest, OperationResponse
from app.repository.wallets import get_all_wallets, add_income as add_income_db, is_wallet_exist, get_walled_balance_by_name, add_expense as add_expense_db, get_wallet_by_id
from app.repository.operations import create_operation, get_operations_list as get_operations_from_db
from app.models import User

def add_income(db: Session, current_user: User, operation: OperationRequest) -> OperationResponse:

    if not is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"walled {operation.wallet_name} not found"
        )
        
    wallet = add_income_db(db, current_user.id, operation.wallet_name, operation.amount)
    operation = create_operation(
        db=db,
        wallet_id=wallet.id,
        type="income",
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description
    )
    
    db.commit()

    return OperationResponse.model_validate(operation)

def add_expense(db: Session, current_user: User, operation: OperationRequest) -> OperationResponse:

    if not is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"walled {operation.wallet_name} not found"
        )
        
        
    wallet = get_walled_balance_by_name(db, current_user.id, operation.wallet_name)
    if wallet.balanse < operation.amount:
        
        raise HTTPException(
            status_code=400,
            detail=f"insufficient funds. availble: {wallet.balanse}"
        )
    
    wallet = add_expense_db(db, current_user.id, operation.wallet_name, operation.amount)
    
    operation = create_operation(
        db=db,
        wallet_id=wallet.id,
        type="expense",
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description
    )
    db.commit()
    
    return OperationResponse.model_validate(operation)


def get_operations_list(
    db : Session,
    current_user: User,
    wallet_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None
) -> list[OperationResponse]:
    
    if wallet_id:
        wallet = get_wallet_by_id(db , current_user.id, wallet_id)
        
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail=f"Wallet {wallet_id} not found"
            )

        wallets_ids = [wallet.id]
        
    else:
        wallets = get_all_wallets(db, current_user.id)
        wallets_ids = [w.id for w in wallets]
        
    operations = get_operations_from_db(
        db, 
        wallets_ids,
        date_from,
        date_to
    )
    
    result = []
    
    for operation in operations:
        result.append(OperationResponse.model_validate(operation))
        
    return result
