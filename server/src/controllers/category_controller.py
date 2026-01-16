from typing import List, Dict, Any
from ..dao.category_dao import CategoryDAO

class CategoryController:
    def __init__(self):
        self.category_dao = CategoryDAO()

    def get_all_categories(self) -> List[Dict[str, Any]]:
        """
        Retrieve all categories with validation.

        Returns:
            List of category dictionaries with nested subcategories

        Raises:
            Exception: If there's an error retrieving categories
        """
        try:
            categories = self.category_dao.get_all_categories()

            # Validate the category structure
            self._validate_category_structure(categories)

            return categories

        except Exception as e:
            raise Exception(f"Error retrieving categories: {str(e)}")

    def _validate_category_structure(self, categories: List[Dict[str, Any]]) -> None:
        """
        Validate the structure of category data.

        Args:
            categories: List of category dictionaries to validate

        Raises:
            ValueError: If validation fails
        """
        if not isinstance(categories, list):
            raise ValueError("Categories data must be a list")

        for category in categories:
            if not isinstance(category, dict):
                raise ValueError("Each category must be a dictionary")

            # Check required fields
            if 'id' not in category:
                raise ValueError("Category missing required 'id' field")
            if 'name' not in category:
                raise ValueError("Category missing required 'name' field")

            # Validate field types
            if not isinstance(category['id'], str):
                raise ValueError("Category 'id' must be a string")
            if not isinstance(category['name'], str):
                raise ValueError("Category 'name' must be a string")

            # Validate subcategories if present
            if 'subcategories' in category:
                if not isinstance(category['subcategories'], list):
                    raise ValueError("Category 'subcategories' must be a list")
                self._validate_category_structure(category['subcategories'])
