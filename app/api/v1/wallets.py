from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import CreateWalletRequest
from app.service import wallets as wallets_service
from app.dependecy import get_db, get_current_user
from app.models import User

router = APIRouter()

@router.get("/balanse")
def get_balanse(walled_name: str | None = None, db: Session = Depends(get_db), 
                current_user: User = Depends(get_current_user)):
    return wallets_service.get_wallets(db, current_user, walled_name)
  
@router.post("/wallets")
def create_wallet(wallet_request: CreateWalletRequest, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    
    return wallets_service.create_wallet(db, current_user, wallet_request)
    
