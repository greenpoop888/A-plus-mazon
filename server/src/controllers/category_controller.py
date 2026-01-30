from typing import List, Optional
from sqlmodel import Session
from ..dao.category_dao import CategoryDAO
from ..models import Category

class CategoryController:
    def __init__(self, session: Session):
        self.category_dao = CategoryDAO(session)

    def get_all_categories(self) -> List[Category]:
        try:
            return self.category_dao.get_all()
        except Exception as e:
            raise Exception(f"Controller retrive cateogires error: {str(e)}")

    def get_category_tree(self) -> List[dict]:
        flat_categories = self.category_dao.get_all()
        
        category_map = {c.id: {**c.model_dump(), "subcategories": []} for c in flat_categories}
        
        tree = []

        for c in flat_categories:
            cat_id = c.id
            parent_id = c.parent_id
            
            if parent_id is None:
                tree.append(category_map[cat_id])
            else:
                if parent_id in category_map:
                    category_map[parent_id]["subcategories"].append(category_map[cat_id])
        
        return tree

    def get_primary_categories(self) -> List[Category]:
        return self.category_dao.get_by_level("primary")

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.category_dao.get_by_id(category_id)