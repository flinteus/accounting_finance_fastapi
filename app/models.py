from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal

from app.database import Base

class User(Base):
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[int] = mapped_column(unique=True)
    

class Wallet(Base):
    
    __tablename__ = "wallets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    balanse: Mapped[Decimal]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
