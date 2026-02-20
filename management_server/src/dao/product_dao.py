from typing import List, Optional
from ..models.product import Product
from ..models.product_in_store import ProductInStore
from ..models.product_line import ProductLine
from sqlmodel import Session, select, col
from typing import List, Dict, Any
from sqlalchemy.orm import joinedload
from sqlalchemy import func, case, delete


class ProductDAO:
    def __init__(self, session: Session):
        self.session = session

    from sqlalchemy.orm import joinedload

    def get_products(
        self,
        store_id: int
    ) -> List[Dict[str, Any]]:
        """Retrieve products for a given store"""
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
                joinedload(Product.product_line)
            )
            .where(ProductInStore.store_id == store_id)
        )
        
        rows = self.session.exec(statement).unique().all()
        
        results = []
        for row in rows:
            p = row[0]
            final_rate = row[1]
            p_dict = p.model_dump()
            
            p_dict["final_sale_rate"] = float(final_rate)
            p_dict["is_effectively_on_sale"] = final_rate < 0.999
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
    
    def update_quantities(self, store_id: int, update_items: List[dict]) -> bool:
        """Update product quantities for a given store based on the provided update items."""
        try:
            existing_items_stmt = select(ProductInStore).where(ProductInStore.store_id == store_id)
            existing_items_results = self.session.exec(existing_items_stmt).all()
            
            inventory_map = {item.product_id: item for item in existing_items_results}

            for item in update_items:
                p_id = item.get("product_id")
                qty = item.get("quantity")
                
                if p_id is None or qty is None:
                    continue

                if p_id in inventory_map:
                    inventory_map[p_id].quantity = qty
                else:
                    new_entry = ProductInStore(
                        store_id=store_id, 
                        product_id=p_id, 
                        quantity=qty
                    )
                    self.session.add(new_entry)

            self.session.commit()
            return True

        except Exception as e:
            self.session.rollback()
            raise Exception(f"DAO update quantities error: {str(e)}")

    def remove_products_from_store(self, store_id: int, product_ids: List[int]) -> bool:
        """Remove products from a store based on the provided product IDs."""
        try:
            statement = delete(ProductInStore).where(
                (ProductInStore.store_id == store_id) &
                (ProductInStore.product_id.in_(product_ids))
            )
            
            self.session.exec(statement)
            self.session.commit()
            return True
            
        except Exception as e:
            self.session.rollback()
            raise Exception(f"DAO delete products error: {str(e)}")
        
    def get_unoffered_products(self, store_id: int) -> List[dict]:
        """Retrieve products that are not offered in the given store."""
        subquery = select(ProductInStore.product_id).where(ProductInStore.store_id == store_id)
        statement = select(Product).where(~Product.id.in_(subquery))
        products = self.session.exec(statement).all()
        return [product.model_dump() for product in products]