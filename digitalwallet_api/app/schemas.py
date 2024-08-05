from pydantic import BaseModel, Field
from typing import Optional

class WalletCreate(BaseModel):
    owner_name: str
    balance: float = Field(default=0.0, gt=0.0)

class WalletUpdate(BaseModel):
    owner_name: Optional[str] = None
    balance: Optional[float] = Field(default=None, gt=0.0)

class WalletResponse(BaseModel):
    id: int
    owner_name: str
    balance: float

class TransactionCreate(BaseModel):
    wallet_id: int
    amount: float
    type: str  # "deposit" or "withdraw"
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    wallet_id: int
    amount: float
    type: str
    description: Optional[str]
