import asyncio
import contextlib
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401
from app.api.router import api_router
from app.core.config import settings
from app.db import Base, SessionLocal, engine
from app.db.seed import seed_demo_data
from app.services.quotes import sync_quotes_once


logger = logging.getLogger(__name__)


async def quote_sync_loop() -> None:
    while True:
        try:
            with SessionLocal() as session:
                sync_quotes_once(session)
        except Exception as exc:
            logger.warning("Quote sync failed: %s", exc)
        await asyncio.sleep(settings.quote_sync_interval_seconds)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        seed_demo_data(session)

    task = None
    if settings.quote_sync_enabled:
        task = asyncio.create_task(quote_sync_loop())
    try:
        yield
    finally:
        if task:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API for personal investment portfolio tracking and planning.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} API is running"}
