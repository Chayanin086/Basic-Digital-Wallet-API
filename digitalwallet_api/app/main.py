from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI()

create_db_and_tables()

# Define OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Mock user database
fake_users_db = {
    "user@example.com": {
        "username": "user@example.com",
        "full_name": "John Doe",
        "email": "user@example.com",
        "hashed_password": pwd_context.hash("password"),
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

def get_session():
    with Session(engine) as session:
        yield session

# Secure all the existing endpoints with OAuth2 authentication
@app.post("/wallets", response_model=WalletResponse, tags=["Wallet"])
def create_new_wallet(wallet: WalletCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_wallet = Wallet.from_orm(wallet)
    return create_wallet(session, db_wallet)

@app.get("/wallets/{wallet_id}", response_model=WalletResponse, tags=["Wallet"])
def read_wallet(wallet_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_wallet = get_wallet(session, wallet_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet

@app.put("/wallets/{wallet_id}", response_model=WalletResponse, tags=["Wallet"])
def update_existing_wallet(wallet_id: int, wallet: WalletUpdate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_wallet = get_wallet(session, wallet_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return update_wallet(session, wallet_id, wallet.dict(exclude_unset=True))

@app.delete("/wallets/{wallet_id}", tags=["Wallet"])
def delete_existing_wallet(wallet_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_wallet = get_wallet(session, wallet_id)
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    delete_wallet(session, wallet_id)
    return {"message": "Wallet deleted successfully"}

@app.post("/transactions", response_model=TransactionResponse, tags=["Transaction"])
def create_new_transaction(transaction: TransactionCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_transaction = Transaction.from_orm(transaction)
    return create_transaction(session, db_transaction)

@app.get("/wallets/{wallet_id}/transactions", response_model=list[TransactionResponse], tags=["Transaction"])
def read_transactions(wallet_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    transactions = get_transactions_by_wallet(session, wallet_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="Transactions not found")
    return transactions

@app.post("/merchants", response_model=MerchantResponse, tags=["Merchant"])
def create_new_merchant(merchant: MerchantCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_merchant = Merchant.from_orm(merchant)
    return create_merchant(session, db_merchant)

@app.get("/merchants/{merchant_id}", response_model=MerchantResponse, tags=["Merchant"])
def read_merchant(merchant_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_merchant = get_merchant(session, merchant_id)
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return db_merchant

@app.put("/merchants/{merchant_id}", response_model=MerchantResponse, tags=["Merchant"])
def update_existing_merchant(merchant_id: int, merchant: MerchantCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_merchant = get_merchant(session, merchant_id)
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return update_merchant(session, merchant_id, merchant.dict(exclude_unset=True))

@app.delete("/merchants/{merchant_id}", tags=["Merchant"])
def delete_existing_merchant(merchant_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_merchant = get_merchant(session, merchant_id)
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    delete_merchant(session, merchant_id)
    return {"message": "Merchant deleted successfully"}

@app.post("/items", response_model=ItemResponse, tags=["Item"])
def create_new_item(item: ItemCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_item = Item.from_orm(item)
    return create_item(session, db_item)

@app.get("/items/{item_id}", response_model=ItemResponse, tags=["Item"])
def read_item(item_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_item = get_item(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=ItemResponse, tags=["Item"])
def update_existing_item(item_id: int, item: ItemCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_item = get_item(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return update_item(session, item_id, item.dict(exclude_unset=True))

@app.delete("/items/{item_id}", tags=["Item"])
def delete_existing_item(item_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_item = get_item(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    delete_item(session, item_id)
    return {"message": "Item deleted successfully"}
