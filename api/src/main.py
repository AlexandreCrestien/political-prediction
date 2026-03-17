from fastapi import FastAPI, Request
from api.v1.routers.api import api_router

app = FastAPI(
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}