from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlmodel import Session
from ..database.database import get_session
from ..auth.auth import get_current_user
from ..controllers.report_controller import ReportController

router = APIRouter()

@router.get("/api/report/{task_id}/files")
async def get_files(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
    page: int = Query(..., description="page number"),
    page_size: int = Query(..., description="number of items per page")
):
    
    user_id = current_user.get("sub")
    controller = ReportController(session)
    return controller.get_user_reports(user_id=user_id, task_id=task_id, page=page, page_size=page_size)

