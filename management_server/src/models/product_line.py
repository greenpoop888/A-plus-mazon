from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class ProductLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    on_sale: bool = Field(default=False)
    sale_rate: Optional[float] = Field(default=1.0, description="Discount rate if on sale") 

    products: List["Product"] = Relationship(back_populates="product_line")