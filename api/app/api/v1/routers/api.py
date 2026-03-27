from fastapi import APIRouter
from app.api.v1.endpoints.prediction_endpoints import router as prediction_router
from app.api.v1.endpoints.model_endpoints import router as model_router
from app.api.v1.endpoints.communes_endpoints import router as commune_router

api_router = APIRouter()
api_router.include_router(prediction_router)
api_router.include_router(model_router)
api_router.include_router(commune_router) 