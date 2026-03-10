from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.products_route import router as products_router
from src.routes.stores_route import router as stores_router
from src.routes.categories_route import router as categories_route
from src.routes.subscription_route import router as subscription_route
from src.routes.report_route import router as report_route

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(stores_router)
app.include_router(categories_route)
app.include_router(subscription_route)
app.include_router(report_route)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
