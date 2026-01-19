from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from ..models.product import Product
from ..controllers.product_controller import ProductController

router = APIRouter()
product_controller = ProductController()

@router.get("/api/product", response_model=List[Product])
async def get_products(
    primary_category: Optional[str] = Query(None, description="Filter by primary category ID"),
    secondary_category: Optional[str] = Query(None, description="Filter by secondary category ID"),
    tertiary_category: Optional[str] = Query(None, description="Filter by tertiary category ID")
):
    """
    Retrieve a list of products with optional filtering by category.
    """
    try:
        return product_controller.get_products(
            primary_category=primary_category,
            secondary_category=secondary_category,
            tertiary_category=tertiary_category
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
