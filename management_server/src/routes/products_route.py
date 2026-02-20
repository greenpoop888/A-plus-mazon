from fastapi import APIRouter, Query, HTTPException, Depends, Body
from typing import Optional, List, Dict, Any
from ..models.product import Product
from ..controllers.product_controller import ProductController
from ..database.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("/api/products")
async def get_products(
    session: Session = Depends(get_session),
    store_id: int = Query(..., description="Store ID to filter products")
):
    """
    Retrieve a list of products with optional filtering by category.
    """
    try:
        controller = ProductController(session)
        return controller.get_products_by_store(
            store_id=store_id
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

@router.put("/api/quantities")
async def update_quantities(
    payload: Dict[str, Any] = Body(...),
    session: Session = Depends(get_session)
):
    """
    Json format example:
    {
        "store_id": 1,
        "update_items": [{"product_id": 101, "quantity": 10}, ...]
    }
    """
    try:
        store_id = payload.get("store_id")
        update_items = payload.get("update_items", [])

        if store_id is None:
            raise ValueError("store_id is required")

        controller = ProductController(session)
        
        result = controller.update_product_quantities(
            store_id=store_id,
            items=update_items
        )
        
        return {"status": "success", "updated_items_count": len(update_items)}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.post("/api/products")
async def create_product(
    payload: Dict[str, Any] = Body(...),
    session: Session = Depends(get_session)
):
    """
    Offer new item to the sotre. Json format example:
    {
        "store_id": 1,
        "new_offer": [
            {"product_id": 501, "quantity": 100},
            {"product_id": 502, "quantity": 200}
        ]
    }
    """
    try:
        store_id = payload.get("store_id")
        new_offer = payload.get("new_offer", [])

        if store_id is None:
            raise HTTPException(status_code=400, detail="Missing store_id")

        controller = ProductController(session)
        
        success = controller.update_product_quantities(
            store_id=store_id,
            update_items=new_offer
        )
        
        if success:
            return {
                "status": "success", 
                "message": f"Successfully added/updated {len(new_offer)} products for store {store_id}"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.delete("/api/products")
async def delete_products_from_store(
    payload: Dict[str, Any] = Body(...),
    session: Session = Depends(get_session)
):
    """
    Stop offering certain products in the store. Json format example:
    {
        "store_id": 1,
        "product_ids": [101, 102, 103]
    }
    """
    try:
        store_id = payload.get("store_id")
        product_ids = payload.get("product_ids", [])

        if store_id is None or not product_ids:
            raise HTTPException(status_code=400, detail="Missing store_id or product_ids")

        controller = ProductController(session)
        success = controller.remove_products_from_store(
            store_id=store_id,
            product_ids=product_ids
        )
        
        return {"status": "success", "removed_count": len(product_ids)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        

@router.get("/api/unoffered-products")
async def get_unoffered_products(
    session: Session = Depends(get_session),
    store_id: int = Query(..., description="Store ID to filter unoffered products")
):
    """
    Retrieve a list of products that are not currently offered in the specified store.
    """
    try:
        controller = ProductController(session)
        return controller.get_unoffered_products_by_store(store_id=store_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")