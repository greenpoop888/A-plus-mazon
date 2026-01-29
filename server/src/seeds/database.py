import sys
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel
from models.category import Category
from models.product import Product
from models.store import Store
from models.product_in_store import ProductInStore
from models.product_line import ProductLine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True) 
def create_db_and_tables():
    print(f"connection: {DATABASE_URL.split('@')[-1]}")
    
    detected_tables = SQLModel.metadata.tables.keys()
    if not detected_tables:
        print("warning: no tables were detected in the models. Please check your model definitions.")
        return

    print(f"table list: {', '.join(detected_tables)}")
    
    try:
        SQLModel.metadata.create_all(engine)
        print("all table created successfully!")
    except Exception as e:
        print(f"error: {e}")

def reset_db_tables():
    print("cleaning tables...")
    
    SQLModel.metadata.drop_all(engine)
    print("tables dropped successfully!")

if __name__ == "__main__":
    reset_db_tables()
    create_db_and_tables()