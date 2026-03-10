from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional

class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_cognito_id: str = Field(index=True)
    report_task_id: int = Field(foreign_key="reporttask.id", index=True)
    is_active: bool = Field(default=True) 
    active_time: datetime = Field(default_factory=datetime.utcnow)