from typing import List, Dict, Any
from ..dao.store_dao import StoreDAO

class StoreController:
    def __init__(self):
        self.store_dao = StoreDAO()
    def get_all_stores(self) -> List[Dict[str, Any]]:
        """
        Retrieve all stores with validation.

        Returns:
            List of store dictionaries with nested subcategories

        Raises:
            Exception: If there's an error retrieving categories
        """
        try:
            stores = self.store_dao.get_all_stores()
            return stores

        except Exception as e:
            raise Exception(f"Error retrieving stores: {str(e)}")