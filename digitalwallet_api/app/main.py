from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session
from app.database import engine, create_db_and_tables
from app.models import Wallet, Transaction, Merchant, Item
from app.schemas import (
    WalletCreate, WalletUpdate, WalletResponse,
    TransactionCreate, TransactionResponse,
    MerchantCreate, MerchantResponse,
    ItemCreate, ItemResponse
)
from app.crud import (
    create_wallet, get_wallet, update_wallet, delete_wallet,
    create_transaction, get_transactions_by_wallet,
    create_merchant, get_merchant, update_merchant, delete_merchant,
    create_item, get_item, update_item, delete_item
)

app = FastAPI()

create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/wallets", response_model=WalletResponse)
def create_new_wallet(wallet: WalletCreate, session: Session = Depends(get_session)):
    db_wallet = Wallet.from_orm(wallet)
    return create_wallet(session, db_wallet)

@app.get("/wallets/{wallet_id}", response_model=WalletResponse)
def read_wallet(wallet_id: int, session: Session = Depends(get_session)):
    db_wallet = get_wallet(session, wallet_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet

@app.put("/wallets/{wallet_id}", response_model=WalletResponse)
def update_existing_wallet(wallet_id: int, wallet: WalletUpdate, session: Session = Depends(get_session)):
    db_wallet = get_wallet(session, wallet_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return update_wallet(session, wallet_id, wallet.dict(exclude_unset=True))

@app.delete("/wallets/{wallet_id}")
def delete_existing_wallet(wallet_id: int, session: Session = Depends(get_session)):
    db_wallet = get_wallet(session, wallet_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    delete_wallet(session, wallet_id)
    return {"message": "Wallet deleted successfully"}

@app.post("/transactions", response_model=TransactionResponse)
def create_new_transaction(transaction: TransactionCreate, session: Session = Depends(get_session)):
    db_transaction = Transaction.from_orm(transaction)
    return create_transaction(session, db_transaction)

@app.get("/wallets/{wallet_id}/transactions", response_model=list[TransactionResponse])
def read_transactions(wallet_id: int, session: Session = Depends(get_session)):
    transactions = get_transactions_by_wallet(session, wallet_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="Transactions not found")
    return transactions

@app.post("/merchants", response_model=MerchantResponse)
def create_new_merchant(merchant: MerchantCreate, session: Session = Depends(get_session)):
    db_merchant = Merchant.from_orm(merchant)
    return create_merchant(session, db_merchant)

@app.get("/merchants/{merchant_id}", response_model=MerchantResponse)
def read_merchant(merchant_id: int, session: Session = Depends(get_session)):
    db_merchant = get_merchant(session, merchant_id)
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return db_merchant

@app.put("/merchants/{merchant_id}", response_model=MerchantResponse)
def update_existing_merchant(merchant_id: int, merchant: MerchantCreate, session: Session = Depends(get_session)):
    db_merchant = get_merchant(session, merchant_id)
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return update_merchant(session, merchant_id, merchant.dict(exclude_unset=True))

@app.delete("/merchants/{merchant_id}")
def delete_existing_merchant(merchant_id: int, session: Session = Depends(get_session)):
    db_merchant = get_merchant(session, merchant_id)
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    delete_merchant(session, merchant_id)
    return {"message": "Merchant deleted successfully"}

@app.post("/items", response_model=ItemResponse)
def create_new_item(item: ItemCreate, session: Session = Depends(get_session)):
    db_item = Item.from_orm(item)
    return create_item(session, db_item)

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, session: Session = Depends(get_session)):
    db_item = get_item(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_existing_item(item_id: int, item: ItemCreate, session: Session = Depends(get_session)):
    db_item = get_item(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return update_item(session, item_id, item.dict(exclude_unset=True))

@app.delete("/items/{item_id}")
def delete_existing_item(item_id: int, session: Session = Depends(get_session)):
    db_item = get_item(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    delete_item(session, item_id)
    return {"message": "Item deleted successfully"}
