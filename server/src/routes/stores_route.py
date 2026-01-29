from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..controllers.store_controller import StoreController

router = APIRouter()
store_controller = StoreController()

@router.get("/api/stores", response_model=List[Dict[str, Any]])
async def get_stores():
    """
    Retrieve all stores in hierarchical structure.
    """
    try:
        return store_controller.get_all_stores()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
