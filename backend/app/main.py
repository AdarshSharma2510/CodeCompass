from fastapi import FastAPI

from app.api.health import router as health_router
from app.config.logging import configure_logging
from app.config.settings import settings
from app.api.repository import router as repository_router

configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(health_router)
app.include_router(repository_router)