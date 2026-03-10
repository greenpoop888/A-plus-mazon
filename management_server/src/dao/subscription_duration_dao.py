from typing import List, Dict, Any
from sqlmodel import Session, select, col
from ..models import SubscriptionDuration
from datetime import datetime, timezone

class SubscriptionDurationDAO:
    def __init__(self, session: Session):
        self.session = session

    def resume_subscription(self, session, user_id: str, task_id: int):
            statement = select(SubscriptionDuration).where(
                SubscriptionDuration.user_cognito_id == user_id,
                SubscriptionDuration.report_task_id == task_id,
                SubscriptionDuration.end_at == None
            )
            existing_sub = session.exec(statement).first()
            
            if existing_sub:
                print(f"User {user_id} already has an active subscription for Task {task_id}")
                return existing_sub

            new_sub = SubscriptionDuration(
                user_cognito_id=user_id,
                report_task_id=task_id,
                start_at=datetime.now(timezone.utc),
                end_at=None
            )
            
            session.add(new_sub)
            session.commit()
            session.refresh(new_sub)
            return new_sub
    

    def pause_subscription(self, session, user_id: str, task_id: int):
        statement = select(SubscriptionDuration).where(
            SubscriptionDuration.user_cognito_id == user_id,
            SubscriptionDuration.report_task_id == task_id,
            SubscriptionDuration.end_at == None
        )
        active_sub = session.exec(statement).first()
        
        if not active_sub:
            print(f"No active subscription found for User {user_id}, Task {task_id}")
            return None

        active_sub.end_at = datetime.now(timezone.utc)
        
        session.add(active_sub)
        session.commit()
        session.refresh(active_sub)
        return active_sub