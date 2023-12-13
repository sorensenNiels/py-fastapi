from fastapi import APIRouter

from .ask import router as ask_router
from .health import router as health_router

main_router = APIRouter()

main_router.include_router(ask_router, tags=["question"])
main_router.include_router(health_router, tags=["health"])


@main_router.get("/")
async def index():
    return {"message": "Hello World!"}
