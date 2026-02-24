# Backend Service
Using python3.11 and FastAPI for backend api system.

## Feature 
 - Read Stores
 - Read Offered/unoffer Products (with store_id)
 - Offer new products for a store
 - Unoffer products for a store
 - Edit offered prodcuts quantity fro a store

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
- Swagger UI: `http://localhost:8000/docs`
