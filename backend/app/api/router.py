from fastapi import APIRouter

from app.api.routes_auth import router as auth_router
from app.api.routes_health import router as health_router
from app.api.routes_predict import router as predict_router
from app.api.routes_profile import router as profile_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(profile_router)
api_router.include_router(health_router)
api_router.include_router(predict_router)
