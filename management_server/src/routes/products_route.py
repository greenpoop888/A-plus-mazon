from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, List
from ..models.product import Product
from ..controllers.product_controller import ProductController
from ..database.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("/api/products")
async def get_products(
    session: Session = Depends(get_session),
    store_id: int = Query(..., description="Store ID to filter products"),
    primary_category: Optional[int] = Query(None, description="Filter by primary category ID"),
    secondary_category: Optional[int] = Query(None, description="Filter by secondary category ID"),
    tertiary_category: Optional[int] = Query(None, description="Filter by tertiary category ID")
):
    """
    Retrieve a list of products with optional filtering by category.
    """
    try:
        controller = ProductController(session)
        return controller.get_products_by_store(
            store_id=store_id,
            primary_category=primary_category,
            secondary_category=secondary_category,
            tertiary_category=tertiary_category
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/quantities")
async def get_quantities(
    session: Session = Depends(get_session),
    store_id: int = Query(..., description="Store ID to filter products"),
    product_ids: str = Query(..., description="List of product IDs to get quantities for")
):
    """
    Retrieve quantities for specific products in a store.
    """
    try:
        id_list = [int(pid) for pid in product_ids.split(',')]
        controller = ProductController(session)
        return controller.get_quantities_by_store_and_product_ids(
            store_id=store_id,
            product_ids=id_list
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    tertiary_category: Optional[str] = Query(None, description="Filter by tertiary category ID")

   