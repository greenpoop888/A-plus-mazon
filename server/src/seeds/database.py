import sys
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel
from ..models import Product, Category, Store, ProductLine, ProductInStore, Report, ReportTask, Subscription, Transaction, SubscriptionDuration
from ..config.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True) 
def create_db_and_tables():
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