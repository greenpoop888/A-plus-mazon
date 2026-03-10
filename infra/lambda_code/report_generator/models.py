from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, ARRAY, String, Column

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    report_hash: str
    report_task_id: int
    s3_bucket: str
    s3_key: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ReportTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    target_type: str  # 'store' or 'category'
    target_id: int    
    frequency: str    

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

class ProductInStore(SQLModel, table=True):
    store_id: int = Field(primary_key=True)
    product_id: int = Field(primary_key=True) 
    quantity: int

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    level: str  
    parent_id: Optional[int] = None

class ProductLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    on_sale: bool = False
    sale_rate: Optional[float] = 1.0