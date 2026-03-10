import os
import json
import boto3
from sqlmodel import Session, create_engine, select
from models import ReportTask, Subscription
import urllib.parse

password = urllib.parse.quote_plus(os.getenv('DB_PASSWORD', ''))
DB_URL = f"postgresql+pg8000://dbadmin:{password}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
SQS_URL = os.getenv('SQS_URL')

engine = create_engine(DB_URL, connect_args={"timeout": 10}) 
sqs = boto3.client('sqs')

def handler(event, context):
    target_frequency = event.get('frequency', '1min')
    scheduled_at = event.get('scheduled_at')
    
    print(f"DEBUG: Dispatcher started for frequency: [{target_frequency}]")
    print(f"DEBUG: Scheduled time from EventBridge: {scheduled_at}")

    try:
        with Session(engine) as session:
            statement = (
                select(ReportTask)
                .join(Subscription)
                .where(ReportTask.frequency == target_frequency)
                .where(Subscription.is_active == True)
                .distinct() 
            )
            tasks = session.exec(statement).all()
            
            print(f"DEBUG: Found {len(tasks)} tasks with frequency '{target_frequency}' in DB.")
            
            dispatched_count = 0
            for task in tasks:
                message = {
                    "task_id": task.id,
                    "target_type": task.target_type,
                    "target_id": task.target_id,
                    "frequency": task.frequency,
                    "scheduled_at": scheduled_at
                }
                
                sqs.send_message(
                    QueueUrl=SQS_URL,
                    MessageBody=json.dumps(message)
                )
                dispatched_count += 1
                
            print(f"DEBUG: Successfully sent {dispatched_count} messages to SQS.")
        
        return {
            "statusCode": 200, 
            "body": {
                "dispatched": dispatched_count,
                "frequency": target_frequency,
                "scheduled_at": scheduled_at
            }
        }
    except Exception as e:
        print(f"ERROR in dispatcher: {str(e)}")
        return {"statusCode": 500, "body": str(e)}