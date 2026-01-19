from fastapi import APIRouter

from ai.routers import router as ai_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(router=ai_router, prefix="/ai", tags=["ai"])
