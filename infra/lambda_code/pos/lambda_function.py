import os
import json
import pg8000.native

def get_db_connection():
    return pg8000.native.Connection(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        timeout=5
    )

def to_dict(columns, row):
    return dict(zip([c['name'] for c in columns], row))

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

    conn = None
    try:
        conn = get_db_connection()

        if path == "/inventory" and method == "GET":
            pid = query_params.get('product_id')
            sid = query_params.get('store_id')
            min_amt = int(query_params.get('min_amount', 0))
            
            res = conn.run("SELECT quantity FROM productinstore WHERE store_id = :sid AND product_id = :pid", sid=sid, pid=pid)
            if res:
                current_qty = res[0][0]
                return response(200, {"hasStock": current_qty >= min_amt, "current": current_qty})
            return response(404, {"error": "Not found"})

        elif path == "/price" and method == "GET":
            pid = query_params.get('product_id')
            sid = query_params.get('store_id')
            
            sql = """SELECT p.price, p.on_sale AS p_on_sale, p.sale_rate AS p_sale_rate,
                            pis.quantity, pl.on_sale AS pl_on_sale, pl.sale_rate AS pl_sale_rate
                     FROM product AS p
                     JOIN productinstore AS pis ON p.id = pis.product_id
                     JOIN productline AS pl ON p.product_line_id = pl.id
                     WHERE p.id = :pid AND pis.store_id = :sid"""
            
            res = conn.run(sql, pid=pid, sid=sid)
            if res:
                columns = [{"name": "price"}, {"name": "p_on_sale"}, {"name": "p_sale_rate"}, 
                           {"name": "quantity"}, {"name": "pl_on_sale"}, {"name": "pl_sale_rate"}]
                data = to_dict(columns, res[0])
                
                if data['quantity'] <= 0:
                    return response(400, {"error": "Out of stock"})
                
                final_sale = 1.0
                if data['p_on_sale'] or data['pl_on_sale']:
                    p_rate = data['p_sale_rate'] if data['p_on_sale'] else 1.0
                    pl_rate = data['pl_sale_rate'] if data['pl_on_sale'] else 1.0
                    final_sale = min(p_rate, pl_rate)
                
                final_price = round(float(data['price']) * float(final_sale), 2)
                return response(200, {"productId": pid, "price": max(0.0, final_price)})
            return response(404, {"error": "Product not found"})

        elif path == "/deduct" and method == "POST":
            pid, sid, qty = body.get('product_id'), body.get('store_id'), body.get('quantity', 0)
            try:
                res = conn.run("""UPDATE productinstore SET quantity = quantity - :qty 
                                 WHERE store_id = :sid AND product_id = :pid AND quantity >= :qty
                                 RETURNING quantity""", qty=qty, sid=sid, pid=pid)
                if not res:
                    return response(400, {"error": "Insufficient inventory or product not found"})

                sql_p = """
                    SELECT p.barcode, p.name, p.price, 
                           p.primary_category_id, p.secondary_category_id, p.tertiary_category_id,
                           LEAST(
                               CASE WHEN p.on_sale = TRUE THEN p.sale_rate ELSE 1.0 END,
                               CASE WHEN pl.on_sale = TRUE THEN pl.sale_rate ELSE 1.0 END
                           ) as effective_rate
                    FROM product p
                    LEFT JOIN productline pl ON p.product_line_id = pl.id
                    WHERE p.id = :pid
                """
                p_res = conn.run(sql_p, pid=pid)
                cols = [{"name": "bc"}, {"name": "name"}, {"name": "price"}, 
                        {"name": "p1"}, {"name": "p2"}, {"name": "p3"}, {"name": "rate"}]
                p_info = to_dict(cols, p_res[0])
                
                final_price = float(p_info['price']) * float(p_info['rate'])
                revenue = round(final_price * qty, 2)
                
                conn.run("""INSERT INTO transaction (store_id, product_id,product_barcode, product_name, 
                                                   primary_category_id, secondary_category_id, tertiary_category_id, 
                                                   quantity, revenue, timestamp)
                            VALUES (:sid, :pid, :bc, :name, :p1, :p2, :p3, :q, :rev, NOW())""", 
                         sid=sid, pid=pid, bc=p_info['bc'], name=p_info['name'], 
                         p1=p_info['p1'], p2=p_info['p2'], p3=p_info['p3'], 
                         q=qty, rev=revenue)

                conn.run("COMMIT")
                return response(200, {"status": "success", "newQuantity": res[0][0], "revenue": revenue})
            except Exception as e:
                conn.run("ROLLBACK")
                return response(500, {"error": str(e)})

        elif path == "/deduct-batch" and method == "POST":
            sid = body.get('store_id')
            items = body.get('items', [])
            results = [] 
            try:
                for item in items:
                    pid, qty = item['product_id'], item['quantity']
                    res = conn.run("""UPDATE productinstore SET quantity = quantity - :qty 
                                     WHERE store_id = :sid AND product_id = :pid AND quantity >= :qty
                                     RETURNING quantity""", qty=qty, sid=sid, pid=pid)
                    if not res:
                        raise Exception(f"Item {pid} insufficient stock")
                    
                    sql_p = """
                        SELECT p.barcode, p.name, p.price, 
                               p.primary_category_id, p.secondary_category_id, p.tertiary_category_id,
                               LEAST(
                                   CASE WHEN p.on_sale = TRUE THEN p.sale_rate ELSE 1.0 END,
                                   CASE WHEN pl.on_sale = TRUE THEN pl.sale_rate ELSE 1.0 END
                               ) as effective_rate
                        FROM product p
                        LEFT JOIN productline pl ON p.product_line_id = pl.id
                        WHERE p.id = :pid
                    """
                    p_res = conn.run(sql_p, pid=pid)
                    cols = [{"name": "bc"}, {"name": "name"}, {"name": "price"}, 
                            {"name": "p1"}, {"name": "p2"}, {"name": "p3"}, {"name": "rate"}]
                    p_info = to_dict(cols, p_res[0])
                    
                    final_price = float(p_info['price']) * float(p_info['rate'])
                    revenue = round(final_price * qty, 2)
                    
                    conn.run("""INSERT INTO transaction (store_id, product_id, product_barcode, product_name, 
                                                       primary_category_id, secondary_category_id, tertiary_category_id, 
                                                       quantity, revenue, timestamp)
                                VALUES (:sid, :pid, :bc, :name, :p1, :p2, :p3, :q, :rev, NOW())""", 
                             sid=sid, pid=pid, bc=p_info['bc'], name=p_info['name'], 
                             p1=p_info['p1'], p2=p_info['p2'], p3=p_info['p3'], 
                             q=qty, rev=revenue)
                             
                    results.append({"product_id": pid, "new_quantity": res[0][0], "revenue": revenue})
                
                conn.run("COMMIT")
                return response(200, {"status": "batch success", "updated_items": results})
            except Exception as e:
                conn.run("ROLLBACK")
                return response(400, {"error": str(e)})

        elif path == "/inventory_need_restock" and method == "GET":
            min_stock = int(query_params.get('min_stock', 10))
            res = conn.run("SELECT store_id, product_id, quantity FROM productinstore WHERE quantity <= :ms", ms=min_stock)
            out = [to_dict([{"name":"store_id"},{"name":"product_id"},{"name":"quantity"}], r) for r in res]
            return response(200, out)

        elif path == "/add" and method == "POST":
            try:
                items = json.loads(event.get('body', '[]'))
                for item in items:
                    sid, pid, amt = item.get('store_id'), item.get('product_id'), int(item.get('add_amount', 0))
                    conn.run("""INSERT INTO productinstore (store_id, product_id, quantity)
                                VALUES (:sid, :pid, :amt)
                                ON CONFLICT (store_id, product_id)
                                DO UPDATE SET quantity = productinstore.quantity + EXCLUDED.quantity""", 
                             sid=sid, pid=pid, amt=amt)
                conn.run("COMMIT")
                return response(200, {"status": "success", "message": "Inventory updated"})
            except Exception as e:
                conn.run("ROLLBACK")
                return response(500, {"status": "error", "message": str(e)})
        else:
            return response(404, {"error": "Route not found"})

    except Exception as e:
        return response(500, {"error": str(e)})
    finally:
        if conn: conn.close()

def response(status_code, data):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }