from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.companions import router as companions_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.health import router as health_router
from app.api.v1.media import router as media_router
from app.api.v1.memory import router as memory_router
from app.api.v1.messages import router as messages_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(companions_router)
api_router.include_router(conversations_router)
api_router.include_router(messages_router)
api_router.include_router(memory_router)
api_router.include_router(media_router)

