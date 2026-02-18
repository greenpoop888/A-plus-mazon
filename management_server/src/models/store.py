from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship 

class Store(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str

    inventories: List["ProductInStore"] = Relationship(back_populates="store")