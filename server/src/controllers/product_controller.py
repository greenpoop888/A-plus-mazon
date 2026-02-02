from typing import List, Optional
from ..models.product import Product
from ..dao.product_dao import ProductDAO
from ..dao.category_dao import CategoryDAO
from sqlmodel import Session

class ProductController:
    def __init__(self, session: Session):
        self.product_dao = ProductDAO(session)
        self.category_dao = CategoryDAO(session)

    def get_products_by_store(
        self,
        store_id: int,
        primary_category: Optional[str] = None,
        secondary_category: Optional[str] = None,
        tertiary_category: Optional[str] = None
    ) -> List[dict]:
    """Retrieve products for a given store with optional category filters."""
        try:
            return self.product_dao.get_products(
                store_id,
                primary_category,
                secondary_category,
                tertiary_category
            )
        except Exception as e:
            raise Exception(f"Controller retrieve products error: {str(e)}")

    def get_quantities_by_store_and_product_ids(
        self,
        store_id: int,
        product_ids: List[int]
    ) -> List[dict]:
    """Retrieve product quantities for a given store and list of product IDs."""
        try:
            return self.product_dao.get_quantities(store_id, product_ids)
        except Exception as e:
            raise Exception(f"Controller retrieve quantities error: {str(e)}")