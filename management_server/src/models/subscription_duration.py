from datetime import datetime
from sqlmodel import SQLModel, Field, Index
from typing import Optional

class SubscriptionDuration(SQLModel, table=True):
    __table_args__ = (
        Index("idx_user_task_dates", "user_cognito_id", "report_task_id", "start_at", "end_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    
    user_cognito_id: str = Field(index=True)
    report_task_id: int = Field(foreign_key="reporttask.id", index=True)
    
    start_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    end_at: Optional[datetime] = Field(default=None, index=True)