from sqlmodel import Session
from ..dao.report_dao import ReportDAO
from ..dao.subscription_dao import SubscriptionDAO
from ..dao.report_task_dao import ReportTaskDAO
import boto3
from ..config.config import settings # 假設你的 Bucket 放在 config

class ReportController:
    def __init__(self, session: Session):
        self.session = session
        self.task_dao = ReportTaskDAO(session)
        self.sub_dao = SubscriptionDAO(session)
        self.report_dao = ReportDAO(session)
        self.s3_client = boto3.client('s3', region_name=settings.REGION)

    def subscribe_logic(self, user_id: str, payload: dict):
        t_type = payload.get("target_type")
        t_id = payload.get("target_id")
        freq = payload.get("frequency")

        task = self.task_dao.get_task(t_type, t_id, freq)
        if not task:
            task = self.task_dao.create_task(t_type, t_id, freq)
        
        return self.sub_dao.subscribe(user_id, task.id)

    def get_user_reports(self, user_id: str, task_id: int, page: int = 1, page_size: int = 10):
        data = self.report_dao.get_reports_by_task(
            self.session, 
            user_id, 
            task_id, 
            page, 
            page_size
        )
        
        reports_list = data["items"]
        results = []
        
        for r in reports_list:
            try:
                url = self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': settings.REPORT_BUCKET, 
                        'Key': r.s3_key
                    },
                    ExpiresIn=3600
                )
            except Exception as e:
                print(f"Error generating presigned URL for {r.s3_key}: {e}")
                url = None

            report_data = r.model_dump()
            report_data['download_url'] = url
            results.append(report_data)
            
        return {
            "items": results,
            "total": data["total"],
            "page": data["page"],
            "page_size": data["page_size"],
            "total_pages": data["total_pages"]
        }