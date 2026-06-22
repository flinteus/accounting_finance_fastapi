from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import CreateWalletRequest, WalletResponse
from app.service import wallets as wallets_service
from app.dependecy import get_db, get_current_user
from app.models import User

router = APIRouter()

@router.get("/balanse")
async def get_balanse(db: Session = Depends(get_db), 
                current_user: User = Depends(get_current_user)):
    return await wallets_service.get_total_balance(db, current_user)
  
@router.post("/wallets", response_model=WalletResponse)
def create_wallet(wallet_request: CreateWalletRequest, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    
    return wallets_service.create_wallet(db, current_user, wallet_request)
    
@router.get("/wallets", response_model=list[WalletResponse])
def get_all_wallets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        return wallets_service.get_all_wallets(db, current_user)
