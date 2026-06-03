from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas import CreateWalletRequest
from app.repository.wallets import is_wallet_exist, get_all_wallets, get_walled_balance_by_name, create_wallet  as create_wallet_db
from app.database import SessionLocal
from app.models import User

def get_wallets(db: Session, current_user: User, walled_name: str | None = None):
    
    if walled_name is None:
        wallets = get_all_wallets(db, current_user.id)
        return {"total_balance": sum([w.balanse for w in wallets])}

    if not is_wallet_exist(db, current_user.id, walled_name):
        raise HTTPException(
            status_code=404,
            detail=f"walled {walled_name} not found"
        )

    wallet = get_walled_balance_by_name(db, current_user.id, walled_name)
    return {"wallet": wallet.name, "balanse": wallet.balanse}

def create_wallet(db: Session, current_user: User, wallet_request: CreateWalletRequest):

    if is_wallet_exist(db, current_user.id, wallet_request.name):
        raise HTTPException(
            status_code=400,
            detail=f"walled {wallet_request.name} already exist"
        )
    
    new_wallet =  create_wallet_db(db, current_user.id, wallet_request.name, wallet_request.initial_balanse)
    db.commit()
    
    return{
        "msg": f"wallet {wallet_request.name} cteated",
        "wallet": new_wallet.name,
        "new_balanse": new_wallet.balanse
    }

