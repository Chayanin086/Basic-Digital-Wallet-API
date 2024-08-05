from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class Wallet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_name: str
    balance: float = 0.0
    transactions: list["Transaction"] = Relationship(back_populates="wallet")

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    wallet_id: int = Field(foreign_key="wallet.id")
    amount: float
    type: str  # "deposit" or "withdraw"
    description: Optional[str] = None
    wallet: Optional[Wallet] = Relationship(back_populates="transactions")
    items: list["Item"] = Relationship(back_populates="transaction")

class Merchant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    items: list["Item"] = Relationship(back_populates="merchant")

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    description: Optional[str] = None
    transaction_id: int = Field(foreign_key="transaction.id")
    merchant_id: int = Field(foreign_key="merchant.id")
    transaction: Optional[Transaction] = Relationship(back_populates="items")
    merchant: Optional[Merchant] = Relationship(back_populates="items")
