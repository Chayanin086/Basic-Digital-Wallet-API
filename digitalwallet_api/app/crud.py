from sqlmodel import Session, select
from app.models import Wallet, Transaction, Merchant, Item

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

def create_merchant(session: Session, merchant: Merchant) -> Merchant:
    session.add(merchant)
    session.commit()
    session.refresh(merchant)
    return merchant

def get_merchant(session: Session, merchant_id: int) -> Merchant:
    return session.get(Merchant, merchant_id)

def update_merchant(session: Session, merchant_id: int, merchant_data: dict) -> Merchant:
    merchant = session.get(Merchant, merchant_id)
    for key, value in merchant_data.items():
        setattr(merchant, key, value)
    session.add(merchant)
    session.commit()
    session.refresh(merchant)
    return merchant

def delete_merchant(session: Session, merchant_id: int):
    merchant = session.get(Merchant, merchant_id)
    session.delete(merchant)
    session.commit()

def create_item(session: Session, item: Item) -> Item:
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

def get_item(session: Session, item_id: int) -> Item:
    return session.get(Item, item_id)

def update_item(session: Session, item_id: int, item_data: dict) -> Item:
    item = session.get(Item, item_id)
    for key, value in item_data.items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

def delete_item(session: Session, item_id: int):
    item = session.get(Item, item_id)
    session.delete(item)
    session.commit()
