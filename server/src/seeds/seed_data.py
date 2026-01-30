import os
import sys
import json
from sqlmodel import Session, create_engine
from ..models import Product, Category, Store, ProductLine, ProductInStore
from sqlalchemy import text
from typing import List, Dict, Any
from ..config.config import settings

engine = create_engine(settings.DATABASE_URL)

def clear_data():
    print("cleaning all data from database...")
    tables = [
        "productinstore", 
        "product", 
        "productline", 
        "store", 
        "category"
    ]
    
    with Session(engine) as session:
        for table in tables:
            session.exec(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
        session.commit()
    print("all data cleared successfully!")

def _load_dummy_data(filename) -> List[Dict[str, Any]]:
        dummy_file_path = os.path.join(os.path.dirname(__file__), 'dummy', filename)
        try:
            with open(dummy_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Dummy stores file not found at {dummy_file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing dummy stores data: {e}")
            return []

def seed_from_json(filename, model):
    print(f"Seeding data for {model.__name__} from {filename}...")
    data = _load_dummy_data(filename)
    with Session(engine) as session:
        for item in data:
                new_model = model(**item)
                session.add(new_model)
        
        session.commit()
        print(f"Seeding completed successfully for {model.__name__}.")

if __name__ == "__main__":
    clear_data()
    seed_from_json('categories.json', Category)
    seed_from_json('stores.json', Store)
    seed_from_json('product_line.json', ProductLine)
    seed_from_json('products.json', Product)
    seed_from_json('product_in_store.json', ProductInStore)