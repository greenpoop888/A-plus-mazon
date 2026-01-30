from typing import Optional, List
from sqlmodel import SQLModel, Field, ARRAY, String, Column, Relationship

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    barcode: str
    name: str
    description: str
    price: float
    image_url: str
    ingredients: List[str] = Field(sa_column=Column(ARRAY(String)))
    primary_category_id: int = Field(foreign_key="category.id")
    secondary_category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    tertiary_category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    on_sale: bool
    sale_rate: Optional[float] = None
    product_line_id: Optional[int] = Field(default=None, foreign_key="productline.id")

    inventories: List["ProductInStore"] = Relationship(back_populates="product")
    product_line: "ProductLine" = Relationship(back_populates="products")
    primary_category: "Category" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Product.primary_category_id]"}
    )
    secondary_category: Optional["Category"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Product.secondary_category_id]"}
    )
    tertiary_category: Optional["Category"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Product.tertiary_category_id]"}
    )