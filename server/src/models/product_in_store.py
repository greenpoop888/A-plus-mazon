from sqlalchemy import Index
from sqlmodel import SQLModel, Field, Relationship

class ProductInStore(SQLModel, table=True):
    store_id: int = Field(default=None, primary_key=True, foreign_key="store.id")
    product_id: int = Field(default=None, primary_key=True, foreign_key="product.id") 
    quantity: int

    product: "Product" = Relationship(back_populates="inventories")
    store: "Store" = Relationship(back_populates="inventories")

    __table_args__ = (
        Index("idx_store_product", "store_id", "product_id"),
    )