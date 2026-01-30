from sqlmodel import SQLModel, Field, Relationship

class ProductInStore(SQLModel, table=True):
    product_id: int = Field(default=None, primary_key=True, foreign_key="product.id") 
    store_id: int = Field(default=None, primary_key=True, foreign_key="store.id")
    quantity: int

    product: "Product" = Relationship(back_populates="inventories")
    store: "Store" = Relationship(back_populates="inventories")