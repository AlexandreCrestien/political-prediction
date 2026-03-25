from fastapi import FastAPI
from app.routes import communes

app = FastAPI(
    version="1.0.0"
)
app.include_router(communes.router)

origins = [
    "http://localhost",
    "http://localhost:8080"
]


@app.get("/")
async def root():
    return {"message": "Hello World"}