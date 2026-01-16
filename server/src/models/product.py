from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    barcode: str
    name: str
    description: str
    price: float
    image_url: str
    ingredients: list[str]
    primary_category_id: str
    secondary_category_id: Optional[str] = None
    tertiary_category_id: Optional[str] = None