from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..controllers.category_controller import CategoryController

router = APIRouter()
category_controller = CategoryController()

@router.get("/categories", response_model=List[Dict[str, Any]])
async def get_categories():
    """
    Retrieve all categories in hierarchical structure.
    """
    try:
        return category_controller.get_all_categories()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
