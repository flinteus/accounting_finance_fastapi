from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas import OperationRequest
from app.repository.wallets import add_income as add_income_db, is_wallet_exist, get_walled_balance_by_name, add_expense as add_expense_db
from app.models import User

def add_income(db: Session, current_user: User, operation: OperationRequest):

    if not is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"walled {operation.wallet_name} not found"
        )
        
    wallet = add_income_db(db, current_user.id, operation.wallet_name, operation.amount)
    db.commit()

    return{
        "msg": f"income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balanse": wallet["balanse"]
    }

def add_expense(db: Session, current_user: User, operation: OperationRequest):

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
    db.commit()
    
    return{
        "msg": "Expense added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balanse": wallet["balanse"]
    }
        
