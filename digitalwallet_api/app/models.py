from typing import Optional
from sqlmodel import Field, SQLModel

class Wallet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_name: str
    balance: float = 0.0

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    wallet_id: int = Field(foreign_key="wallet.id")
    amount: float
    type: str  # "deposit" or "withdraw"
    description: Optional[str] = None
