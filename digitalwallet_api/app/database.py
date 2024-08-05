from sqlmodel import SQLModel, create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost/digitalwallet_db"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
