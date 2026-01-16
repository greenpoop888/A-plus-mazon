import json
import os
from typing import List, Optional
from ..models.product import Product

class ProductDAO:
    def __init__(self):
        self.products = self._load_dummy_data()

    def _load_dummy_data(self) -> List[Product]:
        """Load products from dummy data file"""
        dummy_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dummy', 'products.json')
        try:
            with open(dummy_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Product(**item) for item in data]
        except FileNotFoundError:
            print(f"Warning: Dummy data file not found at {dummy_file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing dummy data: {e}")
            return []

    def get_products(
        self,
        primary_category: Optional[str] = None,
        secondary_category: Optional[str] = None,
        tertiary_category: Optional[str] = None
    ) -> List[Product]:
        """
        Retrieve products with optional category filtering.
        Supports up to three levels of category filtering.

        Args:
            primary_category: Filter by primary category ID
            secondary_category: Filter by secondary category ID
            tertiary_category: Filter by tertiary category ID

        Returns:
            List of Product objects matching the criteria
        """
        filtered_products = self.products

        if primary_category:
            filtered_products = [
                p for p in filtered_products
                if p.primary_category_id == primary_category
            ]

        if secondary_category:
            filtered_products = [
                p for p in filtered_products
                if p.secondary_category_id == secondary_category
            ]

        if tertiary_category:
            filtered_products = [
                p for p in filtered_products
                if p.tertiary_category_id == tertiary_category
            ]

        return filtered_products
