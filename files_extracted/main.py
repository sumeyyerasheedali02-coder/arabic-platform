"""
منصة العربية بين يديك — Arabic Learning Platform
FastAPI entry point: `uvicorn main:app`

This module only assembles the application. Features live in `app/routers`,
reusable logic in `app/services`, configuration in `app/config.py`.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routers import ALL_ROUTERS

settings = get_settings()

APP_VERSION = "1.0.0"


async def on_startup() -> None:
    await init_db()
    # First-run bootstrap only: fills a completely empty database with the book
    # content. It never deletes or replaces anything; replacing content is a
    # deliberate command-line operation (see seed_database.py).
    if settings.seed_on_empty_db:
        from seed_database import content_is_empty, seed
        if await content_is_empty():
            await seed()


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
