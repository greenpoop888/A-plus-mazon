import json
import os
from typing import List, Dict, Any

class StoreDAO:
    def __init__(self):
        self.store = self._load_dummy_data()

    def _load_dummy_data(self) -> List[Dict[str, Any]]:
        """Load stores from dummy data file"""
        dummy_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dummy', 'stores.json')
        try:
            with open(dummy_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Dummy stores file not found at {dummy_file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing dummy stores data: {e}")
            return []

    def get_all_stores(self) -> List[Dict[str, Any]]:
        """
        Retrieve all stores in hierarchical structure.

        Returns:
            List of store dictionaries with nested subcategories
        """
        return self.store