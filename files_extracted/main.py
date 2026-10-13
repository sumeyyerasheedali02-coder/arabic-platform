"""
منصة العربية بين يديك — Arabic Learning Platform
FastAPI entry point: `uvicorn main:app`

This module only assembles the application. Features live in `app/routers`,
reusable logic in `app/services`, configuration in `app/config.py`.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routers import ALL_ROUTERS

# Show the application's own INFO messages (migrations applied, first-run content
# load) next to uvicorn's. Has no effect if logging is already configured.
logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s: %(message)s")

settings = get_settings()
logger = logging.getLogger("arabiq")

APP_VERSION = "1.0.0"


async def on_startup() -> None:
    applied = await init_db()
    if applied:
        logger.info("Database migrations applied: %s", ", ".join(applied))
    # First-run bootstrap only: fills a completely empty database with the base
    # content. It never deletes or replaces anything; replacing content is a
    # deliberate command-line operation (python -m tools.seed --help).
    if settings.seed_on_empty_db:
        from tools.seed import seed_if_empty

        if await seed_if_empty(log=logger.info):
            logger.info("Empty database: base content loaded.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="منصة العربية بين يديك",
        description="نظام تعلم اللغة العربية للطلاب الأتراك في كلية الإلهيات",
        version=APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {
            "message": "مرحباً بك في منصة العربية بين يديك",
            "version": APP_VERSION,
            "docs": "/docs",
        }

    for router in ALL_ROUTERS:
        app.include_router(router)
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
