from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any
from ..controllers.subscription_controller import SubscriptionController
from ..controllers.report_controller import ReportController
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
    try:
        target_type = payload.get("target_type")
        target_id = payload.get("target_id")
        frequency = payload.get("frequency")
        user_id = current_user.get("sub")

        if not user_id:
            raise HTTPException(status_code=400, detail="User ID (sub) not found in token")
        if target_id is None:
            raise HTTPException(status_code=400, detail="Missing target_id")

        controller = SubscriptionController(session)
        
        success = controller.subscribe(
            user_id,
            target_type=target_type,
            target_id=target_id,
            frequency=frequency
        )
        
        if success:
            return {
                "status": "success", 
                "message": f"Successfully subscribed to {'store' if target_type == 'store' else 'category'} with id {target_id} at {frequency} frequency"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/api/subscriptions")
async def list_my_subs(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_id = current_user.get("sub")
    controller = SubscriptionController(session)
    return controller.get_subscriptions(user_id)

@router.delete("/api/subscriptions/{task_id}")
async def remove_subscription(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_id = current_user.get("sub")
    controller = SubscriptionController(session)
    success = controller.unsubscribe(user_id, task_id)
    return {"success": success}

@router.patch("/api/subscriptions/{task_id}/toggle")
async def toggle_subscription(  
    task_id: int,
    status: bool = Body(..., embed=True),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_id = current_user.get("sub")
    controller = SubscriptionController(session)
    success = controller.toggle_subscription_status(user_id, task_id, status)
    return {"success": success}