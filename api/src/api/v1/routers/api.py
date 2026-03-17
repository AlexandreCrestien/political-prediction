from fastapi import APIRouter
from api.v1.endpoints.prediction_endpoints import router as prediction_router
from api.v1.endpoints.model_endpoints import router as model_router

api_router = APIRouter()
api_router.include_router(prediction_router)
api_router.include_router(model_router)
