import os
import csv
import json
import boto3
import hashlib
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, create_engine, text
from models import Report, ReportTask, Product, ProductInStore, Category, ProductLine
from botocore.config import Config

import urllib.parse
password = urllib.parse.quote_plus(os.getenv('DB_PASSWORD', ''))
DB_URL = f"postgresql+pg8000://dbadmin:{password}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
BUCKET = os.getenv('REPORT_BUCKET')

engine = create_engine(DB_URL, connect_args={"timeout": 10})
s3 = boto3.client(
    's3', 
    config=Config(connect_timeout=5, retries={'max_attempts': 0})
)

def get_time_window(scheduled_at_str, frequency):
    if scheduled_at_str:
        dt_str = scheduled_at_str.replace('Z', '+00:00')
        ref_time = datetime.fromisoformat(dt_str)
    else:
        ref_time = datetime.now(timezone.utc)

    end_time = ref_time.replace(second=0, microsecond=0)

    if frequency == 'minute':
        start_time = end_time - timedelta(minutes=1)
    elif frequency == 'hour':
        end_time = end_time.replace(minute=0)
        start_time = end_time - timedelta(hours=1)
    elif frequency == 'day':
        end_time = end_time.replace(hour=0, minute=0)
        start_time = end_time - timedelta(days=1)
    elif frequency == 'week':
        end_time = (end_time - timedelta(days=end_time.weekday())).replace(hour=0, minute=0)
        start_time = end_time - timedelta(weeks=1)
    elif frequency == 'month':
        end_time = end_time.replace(day=1, hour=0, minute=0)
        last_month_day = end_time - timedelta(days=1)
        start_time = last_month_day.replace(day=1)
    else:
        start_time = end_time - timedelta(days=1)

    return start_time, end_time

def handler(event, context):
    print(f"DEBUG: Generator received {len(event.get('Records', []))} records.")
    for record in event['Records']:
        try:
            task = json.loads(record['body'])
            task_id = task['task_id']
            t_type = task['target_type']
            t_id = task['target_id']
            freq = task.get('frequency', '1min')
            scheduled_at = task.get('scheduled_at')

            start_time, end_time = get_time_window(scheduled_at, freq)
            print(f"DEBUG: Task {task_id} [{freq}] Window: {start_time} to {end_time}")

            if t_type == 'store':
                sql = text("""
                    SELECT id, product_barcode, product_name, quantity, revenue, timestamp 
                    FROM transaction 
                    WHERE store_id = :tid AND timestamp >= :s AND timestamp < :e
                """)
            else:
                sql = text("""
                    SELECT t.id, t.product_barcode, t.product_name, t.quantity, t.revenue, t.timestamp 
                    FROM transaction t 
                    JOIN product p ON t.product_id = p.id 
                    WHERE (
                        p.primary_category_id = :tid OR 
                        p.secondary_category_id = :tid OR 
                        p.tertiary_category_id = :tid
                    ) 
                    AND t.timestamp >= :s AND t.timestamp < :e
                """)

            with Session(engine) as session:
                result = session.execute(sql, {"tid": t_id, "s": start_time, "e": end_time})
                rows = result.all()

                if not rows:
                    print(f"DEBUG: No data for Task {task_id} in this window. Skipping.")
                    continue

                time_label = end_time.strftime('%Y%m%d%H%M')
                file_name = f"report_{task_id}_{time_label}.csv"
                local_path = f"/tmp/{file_name}"
                
                with open(local_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Order ID', 'Product Barcode', 'Product Name', 'Quantity', 'Revenue', 'Timestamp'])
                    writer.writerows(rows)

                s3_key = f"reports/task_{task_id}/{file_name}"
                s3.upload_file(local_path, BUCKET, s3_key)

                r_hash = hashlib.md5(s3_key.encode()).hexdigest()
                new_report = Report(
                    report_task_id=task_id,
                    report_hash=r_hash,
                    s3_bucket=BUCKET,
                    s3_key=s3_key,
                    generated_at=datetime.now(timezone.utc)
                )
                session.add(new_report)
                session.commit()
                
                os.remove(local_path)
                print(f"DEBUG: Task {task_id} finished successfully.")

        except Exception as e:
            print(f"ERROR processing record in Task {task_id if 'task_id' in locals() else 'unknown'}: {str(e)}")

    return {"status": "success"}