from typing import Optional, List
from sqlmodel import SQLModel, Field, ARRAY, String, Column

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    barcode: str
    name: str
    description: str
    price: float
    image_url: str
    
    ingredients: List[str] = Field(sa_column=Column(ARRAY(String)))
    
    primary_category_id: int
    secondary_category_id: Optional[int] = None
    tertiary_category_id: Optional[int] = None
    on_sale: bool
    sale_rate: Optional[float] = None

    product_line_id: Optional[int] = None