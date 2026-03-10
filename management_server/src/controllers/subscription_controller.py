from typing import List, Dict, Any
from ..dao.report_task_dao import ReportTaskDAO
from ..dao.subscription_dao import SubscriptionDAO
from ..dao.subscription_duration_dao import SubscriptionDurationDAO
from sqlmodel import Session

class SubscriptionController:
    def __init__(self, session: Session):
        self.session = session
        self.subscribe_dao = SubscriptionDAO(session)
        self.task_dao = ReportTaskDAO(session)
        self.duration_dao = SubscriptionDurationDAO(session)

    def subscribe(self, user_id: str, target_type: str, target_id: int, frequency: str) -> bool:
        try:
            task = self.task_dao.get_task(target_type=target_type, target_id=target_id, frequency=frequency)
            if not task:
                task = self.task_dao.create_task(target_type=target_type, target_id=target_id, frequency=frequency)

            self.subscribe_dao.subscribe(user_id=user_id, report_task_id=task.id)

            result = self.duration_dao.resume_subscription(self.session, user_id=user_id, task_id=task.id)
            
            return True if result else False
        except Exception as e:
            raise Exception(f"Error subscribing: {str(e)}")
        
    def get_subscriptions(self, user_id: str) -> List[Dict[str, Any]]:
        try:
            return self.subscribe_dao.get_user_subscriptions(user_id=user_id)
        except Exception as e:
            raise Exception(f"Error retrieving subscriptions: {str(e)}")
            
    def unsubscribe(self, user_id: str, task_id: int) -> bool:
        try:
            self.duration_dao.pause_subscription(self.session, user_id=user_id, task_id=task_id)
            return self.subscribe_dao.unsubscribe(user_id=user_id, report_task_id=task_id)
        except Exception as e:
            raise Exception(f"Error unsubscribing: {str(e)}")
        
    def toggle_subscription_status(self, user_id: str, task_id: int, status: bool) -> bool:
        try:
            toggle_result = self.subscribe_dao.toggle_subscription_status(user_id=user_id, report_task_id=task_id, status=status)
            if toggle_result:
                if status:
                    result = self.duration_dao.resume_subscription(self.session, user_id=user_id, task_id=task_id)
                else:
                    result = self.duration_dao.pause_subscription(self.session, user_id=user_id, task_id=task_id)
                return True if result else False
            else:
                return False
        except Exception as e:
            raise Exception(f"Error toggling subscription status: {str(e)}")