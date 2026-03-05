from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class ReportSubscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_cognito_id: str = Field(index=True)
    target_type: str  # 'store' or 'category'
    target_id: int    # store_id or category_id
    frequency: str    # 'minute', 'hour', 'day', 'week', 'month'
    is_active: bool = Field(default=True) 
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    last_sent_at: Optional[datetime] = Field(default=None)