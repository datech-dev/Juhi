import sys
from pathlib import Path
from fastapi import FastAPI, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

# Add services/api to python path to share domain models and providers
api_path = Path(__file__).resolve().parents[2] / "api"
if str(api_path) not in sys.path:
    sys.path.insert(0, str(api_path))

from app.core.config import settings
from app.core.errors import UnauthorizedException
from app.infrastructure.database.session import get_db
from app.handlers.extract_memory import ExtractMemoryTaskPayload, handle_extract_memory_task

app = FastAPI(
    title="Juhi Asynchronous Worker",
    description="Background worker for async tasks: memory extraction, summaries, media jobs",
    version="1.0.0",
)


@app.get("/health")
async def health():
    return {"service": "juhi-worker", "status": "healthy"}


@app.post("/tasks/extract-memory")
async def extract_memory_endpoint(
    payload: ExtractMemoryTaskPayload,
    db: AsyncSession = Depends(get_db),
):
    return await handle_extract_memory_task(payload, db)
