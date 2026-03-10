from sqlmodel import Session, select, func, or_, and_
from ..models import Report, SubscriptionDuration

class ReportDAO:
    def __init__(self, session: Session):
        self.session = session

    def get_reports_by_task(self, session, user_id, task_id, page=1, page_size=10):
        base_statement = (
            select(Report)
            .join(SubscriptionDuration, Report.report_task_id == SubscriptionDuration.report_task_id)
            .where(
                SubscriptionDuration.user_cognito_id == user_id,
                Report.report_task_id == task_id,
                Report.generated_at >= SubscriptionDuration.start_at,
                or_(
                    SubscriptionDuration.end_at == None,
                    Report.generated_at <= SubscriptionDuration.end_at
                )
            )
        )

        count_statement = select(func.count()).select_from(base_statement.subquery())
        total = session.exec(count_statement).one()

        paginated_statement = (
            base_statement
            .order_by(Report.generated_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        
        results = session.exec(paginated_statement).all()

        return {
            "items": results,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size 
        }