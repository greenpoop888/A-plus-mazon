from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from ..controllers.category_controller import CategoryController
from ..database.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("/api/categories", response_model=List[Dict[str, Any]])
async def get_categories(session: Session = Depends(get_session)):
    """
    Retrieve all categories in hierarchical structure.
    """
    try:
        controller = CategoryController(session)
        return controller.get_category_tree()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
