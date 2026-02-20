# Backend Service
Using python3.11 and FastAPI for backend api system.

## Feature
 - Read Categories 
 - Read Stores
 - Read Products (with store_id and optional categories filter)
 - Read quantities (with store_id and product_ids)

## Setup
1. install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

The service will be available at `http://localhost:8000`


## API Documentation
Once the service is running, visit for more documentation and endpoints test:
- Swagger UI: `http://localhost:8001/docs`

1. GET /api/products - Get products in store
     parameter:
        - store_id(int): required
        - primary_category(int): optional
        - secondary_category(int): optional
        - tertiary_category(int): optional
        example request url: "http://127.0.0.1:8001/api/products?store_id=1&primary_category=1&secondary_category=1&tertiary_category=1"
2. GET /api/quantities - Get Quantities for products in store
    parameter:
        - store_id(int): required
        - product_ids(string): required, e.g. "1,2,3"
        example request url: "http://127.0.0.1:8001/api/quantities?store_id=1&product_ids=1%2C2"
3. GET /api/categories - Get Categories
    no parameter required
    example request url: "http://127.0.0.1:8001/api/categories"
4. GET /api/stores - Get Stores
    no parameter required
    example request url: "http://127.0.0.1:8001/api/stores"


If you want to connect to RDS server, here is the steps:
1. ssh -i <your_key.pem> ec2-user@<ec2_eip>
2. sudo yum install postgresql15
3. psql -h <your_RDS_Endpoint> -U dbadmin -d grocery
4. \d <table_name>