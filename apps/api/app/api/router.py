from fastapi import APIRouter

from app.api.routes.assets import router as assets_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.plans import router as plans_router
from app.api.routes.transactions import router as transactions_router


api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(assets_router, prefix="/assets", tags=["assets"])
api_router.include_router(plans_router, prefix="/plans", tags=["plans"])
api_router.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
