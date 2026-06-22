from fastapi import HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from app.schemas import CreateWalletRequest, WalletResponse, TotalBalanse
from app.repository.wallets import is_wallet_exist, get_all_wallets as servise_get_all_wallets, get_walled_balance_by_name, create_wallet  as create_wallet_db
from app.models import User
from app.enum import CurrencyEnum
from app.service import exchange_servise

async def get_total_balance(db: Session, current_user: User) -> TotalBalanse:
    
    wallets = get_all_wallets(db, current_user)
    total_balance = Decimal(0)
    
    for wallet in wallets:
        if wallet.currency == CurrencyEnum.RUB:
            total_balance += wallet.balanse
            
        else:
            exchange_rate = await exchange_servise.get_exchange_rate(wallet.currency, CurrencyEnum.RUB)
            total_balance += wallet.balanse * exchange_rate
            
    return TotalBalanse(total_balance=total_balance)

def create_wallet(db: Session, current_user: User, wallet_request: CreateWalletRequest) -> WalletResponse:

    if is_wallet_exist(db, current_user.id, wallet_request.name):
        raise HTTPException(
            status_code=400,
            detail=f"walled {wallet_request.name} already exist"
        )
    
    new_wallet =  create_wallet_db(db, current_user.id, wallet_request.name, 
                                   wallet_request.initial_balanse, wallet_request.currency)
    db.commit()
    
    return WalletResponse.model_validate(new_wallet)

def get_all_wallets(db: Session, current_user: User) -> list[WalletResponse]:
    wallets = servise_get_all_wallets(db, current_user.id)
    
    return [WalletResponse.model_validate(wallet) for wallet in wallets]
