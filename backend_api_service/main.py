from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoint import router as admin_router
from mongo_db_config import check_db_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

app.include_router(admin_router)

# check mongodb connection
check_db_connection()

print("Backend_api_service up and running🚀")

@app.get('/healthz')
async def root():
    return {"msg": "Backend_api_service up and Runnning..."}