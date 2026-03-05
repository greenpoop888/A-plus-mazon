from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 報表的唯一識別標籤 (用來檢查這份報表是否已經產生過)
    # 例如：store_1_minute_202603040930
    report_hash: str = Field(index=True, unique=True)
    
    target_type: str  # 'store' or 'category'
    target_id: int
    frequency: str    # 'minute', 'hour', 'day', 'week', 'month'
    
    s3_bucket: str
    s3_key: str
    
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True
    )