from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoint import router as user_router
from init_db import create_tables

# create sqlite tables
create_tables()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

app.include_router(user_router)

print("Frontend_api_service up and running 🚀")

@app.get('/healthz')
async def root():
    return {"msg": "Backend_api_service up and Runnning..."}