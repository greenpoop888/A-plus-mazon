from typing import List, Optional
from sqlmodel import Session, select, col
from ..models import Category

class CategoryDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Category]:
        statement = select(Category)
        return self.session.exec(statement).all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.session.get(Category, category_id)

    def get_by_level(self, level: str) -> List[Category]:
        statement = select(Category).where(Category.level == level)
        return self.session.exec(statement).all()

    def get_subcategories(self, parent_id: int) -> List[Category]:
        statement = select(Category).where(Category.parent_id == parent_id)
        return self.session.exec(statement).all()

    def get_by_name(self, name: str) -> Optional[Category]:
        statement = select(Category).where(col(Category.name).ilike(f"%{name}%"))
        return self.session.exec(statement).first()

    def create(self, category_data: Category) -> Category:
        self.session.add(category_data)
        self.session.commit()
        self.session.refresh(category_data)
        return category_data