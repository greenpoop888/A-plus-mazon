from typing import Optional
from sqlmodel import SQLModel, Field, ARRAY, String, Column

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    level: str  = Field(index=True) # e.g., 'primary', 'secondary', 'tertiary'
    parent_id: Optional[int] = Field(default=None, index=True)

