import json
import os
from typing import List, Dict, Any

class CategoryDAO:
    def __init__(self):
        self.categories = self._load_dummy_data()

    def _load_dummy_data(self) -> List[Dict[str, Any]]:
        """Load categories from dummy data file"""
        dummy_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dummy', 'categories.json')
        try:
            with open(dummy_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Dummy categories file not found at {dummy_file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing dummy categories data: {e}")
            return []

    def get_all_categories(self) -> List[Dict[str, Any]]:
        """
        Retrieve all categories in hierarchical structure.

        Returns:
            List of category dictionaries with nested subcategories
        """
        return self.categories