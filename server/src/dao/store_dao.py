from typing import List
from sqlmodel import Session, select, col
from ..models import Store

class StoreDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_all_stores(self) -> List[Store]:
        statement = select(Store)
        return self.session.exec(statement).all()