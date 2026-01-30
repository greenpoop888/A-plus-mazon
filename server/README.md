# Backend Service
Using python3.11 and FastAPI for backend api system.

## Feature
 - Read Categories
 - Read Products (with optional categories filter)

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

Once the service is running, visit:
- Swagger UI: `http://localhost:8000/docs`

## Seed data set up
```bash
cd server
python -m src.seeds.database
python -m src.seeds.seed_data
```