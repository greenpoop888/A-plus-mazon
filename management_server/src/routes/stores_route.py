from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from ..controllers.store_controller import StoreController
from ..database.database import get_session
from sqlmodel import Session
from ..auth.auth import get_current_user

router = APIRouter()

@router.get("/api/stores", response_model=List[Dict[str, Any]])
async def get_stores(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)):
    """
    Retrieve all stores in hierarchical structure.
    """
    try:
        controller = StoreController(session)
        return controller.get_all_stores()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
