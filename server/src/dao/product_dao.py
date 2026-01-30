from typing import List, Optional
from ..models.product import Product
from ..models.product_in_store import ProductInStore
from sqlmodel import Session, select, col
from typing import List, Dict, Any
from sqlalchemy.orm import joinedload


class ProductDAO:
    def __init__(self, session: Session):
        self.session = session

    from sqlalchemy.orm import joinedload

    def get_products(
        self,
        store_id: int,
        primary_category: Optional[int] = None,
        secondary_category: Optional[int] = None,
        tertiary_category: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        statement = (
            select(Product)
            .join(ProductInStore)
            .options(
                joinedload(Product.primary_category),
                joinedload(Product.secondary_category),
                joinedload(Product.tertiary_category),
                joinedload(Product.product_line)
            )
            .where(ProductInStore.store_id == store_id)
        )

        if primary_category:
            statement = statement.where(Product.primary_category_id == primary_category)
        if secondary_category:
            statement = statement.where(Product.secondary_category_id == secondary_category)
        if tertiary_category:   
            statement = statement.where(Product.tertiary_category_id == tertiary_category)
        
        products = self.session.exec(statement).unique().all()

        results = []
        for p in products:
            p_dict = p.model_dump()
            p_dict["primary_category_name"] = p.primary_category.name if p.primary_category else None
            p_dict["product_line_name"] = p.product_line.name if p.product_line else None
            results.append(p_dict)

        return results


    def get_product_quantity(self, store_id: int, product_id: int) -> Optional[int]:
        statement = select(ProductInStore).where(
            (ProductInStore.store_id == store_id) &
            (ProductInStore.product_id == product_id)
        )
        product_in_store = self.session.exec(statement).first()
        if product_in_store:
            return product_in_store.quantity
        return None