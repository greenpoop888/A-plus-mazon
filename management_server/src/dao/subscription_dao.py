from typing import Optional
from sqlmodel import Session, select
from ..models import ReportSubscription

class SubscriptionDAO:
    def __init__(self, session: Session):
        self.session = session

    def subscribe(
        self, 
        user_id: str, 
        store_id: Optional[int] = None, 
        category_id: Optional[int] = None, 
        frequency: str = "day"
    ) -> bool:
        try:
            if store_id is not None:
                t_type = "store"
                t_id = store_id
            elif category_id is not None:
                t_type = "category"
                t_id = category_id
            else:
                print("Error: Either store_id or category_id must be provided.")
                return False

            new_sub = ReportSubscription(
                user_cognito_id=user_id,
                target_type=t_type,
                target_id=t_id,
                frequency=frequency
            )

            self.session.add(new_sub)
            self.session.commit()
            self.session.refresh(new_sub)
            return True

        except Exception as e:
            print(f"Error creating subscription: {e}")
            self.session.rollback()
            return False
        
    def get_subscriptions(self, user_id: str):
        try:
            statement = select(ReportSubscription).where(ReportSubscription.user_cognito_id == user_id)
            results = self.session.exec(statement).all()
            return results
        except Exception as e:
            print(f"Error retrieving subscriptions: {e}")
            return []