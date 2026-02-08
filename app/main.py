from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.logger import logger
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    init_db()
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title="URL Shortener",
    lifespan=lifespan,
)

app.include_router(router)
