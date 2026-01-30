from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class ProductLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    products: List["Product"] = Relationship(back_populates="product_line")