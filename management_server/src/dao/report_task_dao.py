from typing import Optional
from sqlmodel import Session, select
from ..models import ReportTask

class ReportTaskDAO:
    def __init__(self, session: Session):
        self.session = session

    # 1. Query if report task exists
    def get_task(self, target_type: str, target_id: int, frequency: str) -> Optional[ReportTask]:
        statement = select(ReportTask).where(
            ReportTask.target_type == target_type,
            ReportTask.target_id == target_id,
            ReportTask.frequency == frequency
        )
        return self.session.exec(statement).first()

    # 2. Create report task
    def create_task(self, target_type: str, target_id: int, frequency: str) -> ReportTask:
        new_task = ReportTask(
            target_type=target_type,
            target_id=target_id,
            frequency=frequency
        )
        self.session.add(new_task)
        self.session.commit()
        self.session.refresh(new_task)
        return new_task