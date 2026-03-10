from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    report_hash: str = Field(index=True, unique=True)
    report_task_id: int = Field(foreign_key="reporttask.id", index=True)
    
    s3_bucket: str
    s3_key: str
    
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True
    )