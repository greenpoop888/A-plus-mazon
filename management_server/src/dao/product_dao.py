from typing import List, Optional
from ..models.product import Product
from ..models.product_in_store import ProductInStore
from ..models.product_line import ProductLine
from sqlmodel import Session, select, col
from typing import List, Dict, Any
from sqlalchemy.orm import joinedload
from sqlalchemy import func, case


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
        """Retrieve products for a given store with optional category filters."""
        statement = (
            select(
                Product,
                func.least(
                    case((Product.on_sale == True, Product.sale_rate), else_=1.0),
                    case((ProductLine.on_sale == True, ProductLine.sale_rate), else_=1.0)
                ).label("effective_rate")
            )
            .join(ProductInStore)
            .outerjoin(ProductLine)
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
        
        rows = self.session.exec(statement).unique().all()
        
        results = []
        for row in rows:
            p = row[0]
            final_rate = row[1]
            p_dict = p.model_dump()
            
            p_dict["final_sale_rate"] = float(final_rate)
            p_dict["is_effectively_on_sale"] = final_rate < 0.999
            p_dict["primary_category_name"] = p.primary_category.name if p.primary_category else None
            p_dict["secondary_category_name"] = p.secondary_category.name if p.secondary_category else None
            p_dict["tertiary_category_name"] = p.tertiary_category.name if p.tertiary_category else None
            p_dict["product_line_name"] = p.product_line.name if p.product_line else None
            results.append(p_dict)

        return results


    def get_quantities(self, store_id: int, product_ids: List[int]) -> List[dict]:
        """Retrieve product quantities for a given store and list of product IDs."""
        statement = select(ProductInStore).where(
            (ProductInStore.store_id == store_id) &
            (ProductInStore.product_id.in_(product_ids))
        )
        product_in_stores = self.session.exec(statement).all()
        if product_in_stores:
            return [{"product_id": pis.product_id, "quantity": pis.quantity} for pis in product_in_stores]
        return []