from sqlmodel import SQLModel, Field, ARRAY, String, Column

class ProductInStore(SQLModel, table=True):
    product_id: int = Field(default=None, primary_key=True)
    store_id: int = Field(default=None, primary_key=True)
    quantity: int