from typing import Optional, List
from sqlmodel import SQLModel, Field, ARRAY, String, Column

class Store(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str