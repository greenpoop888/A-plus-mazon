import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor

def lambda_handler(event, context):
    # 1. 從環境變數讀取資料庫連線資訊 (在 Terraform 中定義的)
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASSWORD')

    # 2. 建立資料庫連線
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass,
            connect_timeout=5
        )
        # 使用 RealDictCursor 可以直接把查詢結果轉成字典格式
        cur = conn.cursor(cursor_factory=RealDictCursor)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Database connection failed: {str(e)}"})
        }

    # 3. 解析來自 API Gateway 的參數
    # 假設路徑是 /inventory?storeId=1&productId=101&minAmount=5
    query_params = event.get('queryStringParameters') or {}
    store_id = query_params.get('storeId')
    product_id = query_params.get('productId')
    min_amount = int(query_params.get('minAmount', 0))

    try:
        # 4. 執行查詢
        # 注意：這裡的 Table Name 和 Column Name 請根據你實際的資料庫修改
        query = """
            SELECT quantity 
            FROM inventory 
            WHERE store_id = %s AND product_id = %s;
        """
        cur.execute(query, (store_id, product_id))
        result = cur.fetchone()

        if result:
            actual_qty = result['quantity']
            # 判斷是否達到要求的最小數量 (minAmount)
            has_enough = actual_qty >= min_amount
            
            response_body = {
                'storeId': store_id,
                'productId': product_id,
                'currentInventory': actual_qty,
                'hasMinAmount': has_enough
            }
            status_code = 200
        else:
            response_body = {'error': 'Product or Store not found'}
            status_code = 404

    except Exception as e:
        response_body = {'error': str(e)}
        status_code = 500
    finally:
        # 5. 關閉連線
        cur.close()
        conn.close()

    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response_body)
    }