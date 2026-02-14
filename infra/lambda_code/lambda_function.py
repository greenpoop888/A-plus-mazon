import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        connect_timeout=5
    )

def lambda_handler(event, context):
    path = event.get('path', '')
    method = event.get('httpMethod', '')
    query_params = event.get('queryStringParameters') or {}
    
    body = {}
    if event.get('body'):
        try:
            body = json.loads(event['body'])
        except:
            pass

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # --- Endpoint 1: GET /inventory ---
        if path == "/inventory" and method == "GET":
            pid = query_params.get('product_id')
            sid = query_params.get('store_id')
            min_amt = int(query_params.get('min_amount', 0))
            
            cur.execute("SELECT quantity FROM productinstore WHERE store_id = %s AND product_id = %s", (sid, pid))
            res = cur.fetchone()
            if res:
                return response(200, {"hasStock": res['quantity'] >= min_amt, "current": res['quantity']})
            return response(404, {"error": "Not found"})

        # --- Endpoint 2: GET /price ---
        elif path == "/price" and method == "GET":
            pid = query_params.get('product_id')
            sid = query_params.get('store_id')
            
            cur.execute("""SELECT p.price, p.on_sale AS p_on_sale, p.sale_rate AS p_sale_rate,
                            pis.quantity, pl.on_sale AS pl_on_sale, pl.sale_rate AS pl_sale_rate
                            FROM product AS p
                            JOIN productinstore AS pis ON p.id = pis.product_id
                            JOIN productline AS pl ON p.product_line_id = pl.id
                            WHERE p.id = %s AND pis.store_id = %s""", (pid, sid))
            res = cur.fetchone()
            
            if res:
                if res['quantity'] <= 0:
                    return response(400, {"error": "Out of stock"})
                
                final_sale = 1.0
                
                if res['p_on_sale'] or res['pl_on_sale']:
                    p_rate = res['p_sale_rate'] if res['p_on_sale'] else 1.0
                    pl_rate = res['pl_sale_rate'] if res['pl_on_sale'] else 1.0
                    final_sale = min(p_rate, pl_rate)
                
                final_price = round(float(res['price']) * float(final_sale), 2)
                
                return response(200, {
                    "productId": pid, 
                    "price": max(0.0, final_price)
                })
            
            return response(404, {"error": "Product not found"})

        # --- Endpoint 3: POST /deduct ---
        elif path == "/deduct" and method == "POST":
            pid, sid, qty = body.get('product_id'), body.get('store_id'), body.get('quantity', 0)
           
            cur.execute("""
                UPDATE productinstore SET quantity = quantity - %s 
                WHERE store_id = %s AND product_id = %s AND quantity >= %s
                RETURNING quantity
            """, (qty, sid, pid, qty))
            
            res = cur.fetchone()
            if res:
                conn.commit()
                return response(200, {"status": "success", "newQuantity": res['quantity']})
            return response(400, {"error": "Insufficient inventory or product not found"})

        # --- Endpoint 4: POST /deduct-batch  ---
        elif path == "/deduct-batch" and method == "POST":
            sid = body.get('store_id')
            items = body.get('items', []) # format: [{"product_id": 1, "quantity": 2}, ...]
            results = [] 

            try:
                cur.execute("BEGIN;")
                for item in items:
                    cur.execute("""
                        UPDATE productinstore 
                        SET quantity = quantity - %s 
                        WHERE store_id = %s AND product_id = %s AND quantity >= %s
                        RETURNING quantity
                    """, (item['quantity'], sid, item['product_id'], item['quantity']))
                    
                    row = cur.fetchone()
                    
                    if row:
                        results.append({
                            "product_id": item['product_id'],
                            "new_quantity": row['quantity']
                        })
                    else:
                        raise Exception(f"Item {item['product_id']} insufficient stock or not found")
                
                conn.commit()
                return response(200, {
                    "status": "batch success",
                    "updated_items": results
                })
            except Exception as e:
                conn.rollback()
                return response(400, {"error": str(e)})

        else:
            return response(404, {"error": "Route not found"})

    except Exception as e:
        return response(500, {"error": str(e)})
    finally:
        if 'conn' in locals(): conn.close()

def response(status_code, data):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }