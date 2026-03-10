from typing import List, Dict, Any
from sqlmodel import Session, select, col
from ..models import Subscription, ReportTask, Store, Category

class SubscriptionDAO:
    def __init__(self, session: Session):
        self.session = session

    def subscribe(self, user_id: str, report_task_id: int) -> bool:
        try:
            statement = select(Subscription).where(
                Subscription.user_cognito_id == user_id,
                Subscription.report_task_id == report_task_id
            )
            sub = self.session.exec(statement).first()

            if sub:
                sub.is_active = True
                self.session.add(sub)
            else:
                sub = Subscription(user_cognito_id=user_id, report_task_id=report_task_id)
                self.session.add(sub)
            
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error subscribing: {e}")
            self.session.rollback()
            raise e

    def get_user_subscriptions(self, user_id: str) -> List[Dict[str, Any]]:
        formatted_results = []
        try:
            store_stmt = (
                select(Subscription, ReportTask, Store.name)
                .join(ReportTask, Subscription.report_task_id == ReportTask.id)
                .join(Store, ReportTask.target_id == Store.id)
                .where(Subscription.user_cognito_id == user_id)
                .where(ReportTask.target_type == "store")
            )
            store_res = self.session.exec(store_stmt).all()
            for sub, task, name in store_res:
                formatted_results.append({
                    **sub.model_dump(),
                    "target_name": name,
                    "task_detail": task.model_dump()
                })

            cat_stmt = (
                select(Subscription, ReportTask, Category.name)
                .join(ReportTask, Subscription.report_task_id == ReportTask.id)
                .join(Category, ReportTask.target_id == Category.id)
                .where(Subscription.user_cognito_id == user_id)
                .where(ReportTask.target_type == "category")
            )
            cat_res = self.session.exec(cat_stmt).all()
            for sub, task, name in cat_res:
                formatted_results.append({
                    **sub.model_dump(),
                    "target_name": name,
                    "task_detail": task.model_dump()
                })

            formatted_results.sort(key=lambda x: x.get('active_time'), reverse=True)
            
            return formatted_results

        except Exception as e:
            print(f"Error fetching subscriptions: {e}")
            return []

    # 5. Unsubscribe (Physical Remove)
    def unsubscribe(self, user_id: str, report_task_id: int) -> bool:
        statement = select(Subscription).where(
            Subscription.user_cognito_id == user_id,
            Subscription.report_task_id == report_task_id
        )
        sub = self.session.exec(statement).first()
        if sub:
            self.session.delete(sub)
            self.session.commit()
            return True
        return False

    # 6. Pause/Toggle Subscription (Logical Update)
    def toggle_subscription_status(self, user_id: str, report_task_id: int, status: bool) -> bool:
        statement = select(Subscription).where(
            Subscription.user_cognito_id == user_id,
            Subscription.report_task_id == report_task_id
        )
        sub = self.session.exec(statement).first()
        if sub:
            sub.is_active = status
            self.session.add(sub)
            self.session.commit()
            return True
        return False
    

    