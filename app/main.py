from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="URL Shortener",
    lifespan=lifespan,
)

app.include_router(router)
