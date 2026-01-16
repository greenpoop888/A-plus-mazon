from typing import List, Optional
from ..models.product import Product
from ..dao.product_dao import ProductDAO
from ..dao.category_dao import CategoryDAO

class ProductController:
    def __init__(self):
        self.product_dao = ProductDAO()
        self.category_dao = CategoryDAO()

    def get_products(
        self,
        primary_category: Optional[str] = None,
        secondary_category: Optional[str] = None,
        tertiary_category: Optional[str] = None
    ) -> List[Product]:
        """
        Retrieve products with optional category filtering and validation.

        Args:
            primary_category: Filter by primary category ID
            secondary_category: Filter by secondary category ID
            tertiary_category: Filter by tertiary category ID

        Returns:
            List of Product objects matching the criteria

        Raises:
            ValueError: If category parameters are invalid
        """
        # Validate category parameters
        self._validate_category_filters(primary_category, secondary_category, tertiary_category)

        # Retrieve products from DAO
        return self.product_dao.get_products(
            primary_category=primary_category,
            secondary_category=secondary_category,
            tertiary_category=tertiary_category
        )

    def _validate_category_filters(
        self,
        primary_category: Optional[str],
        secondary_category: Optional[str],
        tertiary_category: Optional[str]
    ) -> None:
        """
        Validate category filter parameters.

        Args:
            primary_category: Primary category ID to validate
            secondary_category: Secondary category ID to validate
            tertiary_category: Tertiary category ID to validate

        Raises:
            ValueError: If validation fails
        """
        # Basic string validation
        for category, level in [
            (primary_category, "primary"),
            (secondary_category, "secondary"),
            (tertiary_category, "tertiary")
        ]:
            if category is not None:
                if not isinstance(category, str):
                    raise ValueError(f"{level} category must be a string")
                if not category.strip():
                    raise ValueError(f"{level} category cannot be empty")
                if len(category) > 100:  # Reasonable length limit
                    raise ValueError(f"{level} category name too long")

        # Cross-validation: if secondary is provided, primary should be too
        if secondary_category and not primary_category:
            raise ValueError("Primary category must be specified when filtering by secondary category")

        # Cross-validation: if tertiary is provided, secondary should be too
        if tertiary_category and not secondary_category:
            raise ValueError("Secondary category must be specified when filtering by tertiary category")

        # Optional: Check if categories exist in the category data
        # This is commented out for now as it might be expensive, but can be enabled later
        # self._validate_categories_exist(primary_category, secondary_category, tertiary_category)

    def _validate_categories_exist(
        self,
        primary_category: Optional[str],
        secondary_category: Optional[str],
        tertiary_category: Optional[str]
    ) -> None:
        """
        Validate that the provided categories exist in the category data.
        This is an optional validation that can be expensive for large datasets.
        """
        categories = self.category_dao.get_all_categories()

        def find_category(category_id: str, category_list: List[dict], level: str) -> bool:
            for cat in category_list:
                if cat.get('id') == category_id:
                    return True
                if 'subcategories' in cat:
                    if find_category(category_id, cat['subcategories'], level):
                        return True
            return False

        if primary_category and not find_category(primary_category, categories, 'primary'):
            raise ValueError(f"Primary category '{primary_category}' does not exist")

        if secondary_category and not find_category(secondary_category, categories, 'secondary'):
            raise ValueError(f"Secondary category '{secondary_category}' does not exist")

        if tertiary_category and not find_category(tertiary_category, categories, 'tertiary'):
            raise ValueError(f"Tertiary category '{tertiary_category}' does not exist")
