from typing import List, Dict, Any
from ..dao.subscription_dao import SubscriptionDAO
from sqlmodel import Session

class SubscriptionController:
    def __init__(self, session: Session):
        self.subscribe_dao = SubscriptionDAO(session)

    def subscribe(self, user_id: str, store_id: int = None, category_id: int = None, frequency: str = None) -> bool:
        """
        Subscribe to a store or category with a specific frequency.

        Returns:
            True if subscription is successful, False otherwise

        Raises:
            Exception: If there's an error retrieving categories
        """
        try:
            return self.subscribe_dao.subscribe(user_id=user_id, store_id=store_id, category_id=category_id, frequency=frequency)
        except Exception as e:
            raise Exception(f"Error subscribing: {str(e)}")
        
        def get_subscriptions(self, user_id: str) -> List[Dict[str, Any]]:
            """
            Get all subscriptions for a user.

            Returns:
                List of subscriptions with details such as store/category and frequency 
            Raises:
                Exception: If there's an error retrieving subscriptions 
            """
            try:
                return self.subscribe_dao.get_subscriptions(user_id=user_id)
            except Exception as e:
                raise Exception(f"Error retrieving subscriptions: {str(e)}")
            