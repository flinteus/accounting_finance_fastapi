from decimal import Decimal
from sqlalchemy.orm import Session


from app.models import Wallet, User

def is_wallet_exist(db: Session, user_id: int, wallet_name: str) -> bool:

    return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first() is not None

    
def add_income(db: Session, user_id: int, wallet_name: str, amount: float) -> Wallet:
 
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    wallet.balanse += Decimal(str(amount))
    
        
    result = {
        "name": wallet.name,
        "balanse": float(wallet.balanse) 
    }
    return result
    
  

def get_walled_balance_by_name(db: Session, user_id: int, wallet_name: str) -> Wallet:

    return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()


def add_expense(db: Session, user_id: int, wallet_name: str, amount: float) -> Wallet:

    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id == user_id).first()
    wallet.balanse -= Decimal(str(amount))
        
    result = {
        "name": wallet.name,
        "balanse": float(wallet.balanse) 
    }
    return result
    


def get_all_wallets(db: Session, user_id: int) -> list[Wallet]:

    return db.query(Wallet).filter(Wallet.user_id == user_id).all()


def create_wallet(db: Session, user_id: int, wallet_name: str, amount: float) -> Wallet:

    wallet = Wallet(name=wallet_name, balanse=amount, user_id=user_id)
    db.add(wallet)
    db.flush() 
    db.refresh(wallet)
    return wallet
