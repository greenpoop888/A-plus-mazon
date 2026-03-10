from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import Optional

class ReportTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    target_type: str  # 'store' or 'category'
    target_id: int    # store_id or category_id
    frequency: str    # 'minute', 'hour', 'day', 'week', 'month'

class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_cognito_id: str = Field
    report_task_id: int = Field(foreign_key="reporttask.id")
    is_active: bool = Field(default=True) 
    active_time: datetime = Field(default_factory=datetime.utcnow)