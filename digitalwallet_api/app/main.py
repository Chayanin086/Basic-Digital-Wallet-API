from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session
from app.database import engine, create_db_and_tables
from app.models import Wallet, Transaction
from app.schemas import WalletCreate, WalletUpdate, WalletResponse, TransactionCreate, TransactionResponse
from app.crud import create_wallet, get_wallet, update_wallet, delete_wallet, create_transaction, get_transactions_by_wallet

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
