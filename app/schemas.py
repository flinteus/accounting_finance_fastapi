from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from datetime import datetime

from app.enum import CurrencyEnum

class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float = Field(gt=0)
    description: str | None = Field(None, max_length=225)

    @field_validator("wallet_name")
    def wallet_name_not_empty(cls, v: str) -> str:
        v = v.strip()
        
        if not v:
            raise ValueError("wallet name cannot be empty")
    
        return v
    
class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balanse: float = Field(0.0, gt=0)
    
    currency: CurrencyEnum = CurrencyEnum.RUB
    
class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)
    
    
class UserResponse(UserRequest):
    model_config = {"from_attributes": True}
    
    id: int

class WalletResponse(BaseModel):
    model_config = {"from_attributes": True}
    
    id: int
    name: str
    balanse: Decimal
    currency: CurrencyEnum
    
class OperationResponse(BaseModel):
    model_config = {"from_attributes": True}
    
    id: int
    wallet_id: int
    type: str
    amount: Decimal
    currency: CurrencyEnum
    category: str | None
    subcategory: str | None
    created_at: datetime
    
