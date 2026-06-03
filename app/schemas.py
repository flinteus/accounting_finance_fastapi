from pydantic import BaseModel, Field, field_validator

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
    
class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)
    
    
class UserResponse(UserRequest):
    model_config = {"from_attributes": True}
    
    id: int
