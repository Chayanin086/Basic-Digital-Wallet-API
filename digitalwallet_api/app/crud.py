from sqlmodel import Session, select
from app.models import Wallet, Transaction

def create_wallet(session: Session, wallet: Wallet) -> Wallet:
    session.add(wallet)
    session.commit()
    session.refresh(wallet)
    return wallet

def get_wallet(session: Session, wallet_id: int) -> Wallet:
    return session.get(Wallet, wallet_id)

def update_wallet(session: Session, wallet_id: int, wallet_data: dict) -> Wallet:
    wallet = session.get(Wallet, wallet_id)
    for key, value in wallet_data.items():
        setattr(wallet, key, value)
    session.add(wallet)
    session.commit()
    session.refresh(wallet)
    return wallet

def delete_wallet(session: Session, wallet_id: int):
    wallet = session.get(Wallet, wallet_id)
    session.delete(wallet)
    session.commit()

def create_transaction(session: Session, transaction: Transaction) -> Transaction:
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

def get_transactions_by_wallet(session: Session, wallet_id: int):
    statement = select(Transaction).where(Transaction.wallet_id == wallet_id)
    return session.exec(statement).all()
