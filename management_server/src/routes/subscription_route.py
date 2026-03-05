from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any
from ..controllers.subscription_controller import SubscriptionController
from ..database.database import get_session
from sqlmodel import Session
from ..auth.auth import get_current_user

router = APIRouter()

@router.post("/api/subscribe", response_model=Dict[str, Any])
async def subscribe(
    payload: Dict[str, Any] = Body(...),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Subscribe to report. Json format example:
    {
        store_id: 1, # optional, if not provided, subscribe to the category
        category_id: 2,  # optional, if not provided, subscribe to the store
        frequency: "minute"  # or "hour", "day", "week", "month"
    }
    """
    try:
        store_id = payload.get("store_id")
        category_id = payload.get("category_id")
        frequency = payload.get("frequency")
        user_id = current_user.get("sub")

        if not user_id:
            raise HTTPException(status_code=400, detail="User ID (sub) not found in token")
        if store_id is None and category_id is None:
            raise HTTPException(status_code=400, detail="Missing store_id or category_id")

        controller = SubscriptionController(session)
        
        success = controller.subscribe(
            user_id,
            store_id=store_id,
            category_id=category_id,
            frequency=frequency
        )
        
        if success:
            return {
                "status": "success", 
                "message": f"Successfully subscribed to {'store' if store_id else 'category'} with id {store_id or category_id} at {frequency} frequency"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/api/subscriptions", response_model=List[Dict[str, Any]])
async def get_subscriptions(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all subscriptions for the current user
    """
    try:
        user_id = current_user.get("sub")

        if not user_id:
            raise HTTPException(status_code=400, detail="User ID (sub) not found in token")

        controller = SubscriptionController(session)
        subscriptions = controller.get_subscriptions(user_id)
        
        return subscriptions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
