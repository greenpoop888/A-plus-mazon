from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int = Field(foreign_key="store.id", index=True)
    product_id: int = Field(foreign_key="product.id", index=True)
    product_barcode: str
    product_name: str
    primary_category_id: int = Field(foreign_key="category.id", index=True)
    secondary_category_id: Optional[int] = Field(default=None, foreign_key="category.id", index=True)
    tertiary_category_id: Optional[int] = Field(default=None, foreign_key="category.id", index=True)
    quantity: int
    revenue: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)