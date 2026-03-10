from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import Optional

class ReportTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    target_type: str  # 'store' or 'category'
    target_id: int    # store_id or category_id
    frequency: str    # 'minute', 'hour', 'day', 'week', 'month'