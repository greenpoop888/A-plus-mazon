from typing import List, Optional
from ..models.product import Product
from ..dao.product_dao import ProductDAO
from ..dao.category_dao import CategoryDAO
from sqlmodel import Session

class ProductController:
    def __init__(self, session: Session):
        self.product_dao = ProductDAO(session)

    def get_products_by_store(
        self,
        store_id: int
    ) -> List[dict]:
        """Retrieve products for a given store"""
        try:
            return self.product_dao.get_products(
                store_id
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
        
    def update_product_quantities(
        self,
        store_id: int,
        update_items: List[dict]
    ) -> bool:
        """Update product quantities for a given store based on the provided update items."""
        try:
            for item in update_items:
                if "product_id" not in item or "quantity" not in item:
                    raise ValueError("Each update item must contain 'product_id' and 'quantity' fields.")
                if item["quantity"] < 0:
                    raise ValueError("Quantity cannot be negative.")
            return self.product_dao.update_quantities(store_id, update_items)
        except Exception as e:
            raise Exception(f"Controller update quantities error: {str(e)}")

    def remove_products_from_store(self, store_id: int, product_ids: List[int]) -> bool:
        """Remove products from a store based on the provided product IDs."""
        try:
            return self.product_dao.remove_products_from_store(store_id, product_ids)
        except Exception as e:
            raise Exception(f"Controller retrieve quantities error: {str(e)}")
        
    def get_unoffered_products_by_store(self, store_id: int) -> List[dict]:
        """Retrieve products that are not offered in the given store."""
        try:
            return self.product_dao.get_unoffered_products(store_id)
        except Exception as e:
            raise Exception(f"Controller retrieve unoffered products error: {str(e)}")