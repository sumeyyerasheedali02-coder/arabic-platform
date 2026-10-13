"""HTTP routers, one module per feature. All paths live under /api."""
from app.routers import account, admin, auth, chat, content, exercises, progress, srs, teacher
from app.tracking.router import router as tracking_router

ALL_ROUTERS = (
    auth.router,
    account.router,
    content.router,
    exercises.router,
    progress.router,
    srs.router,
    chat.router,
    teacher.router,
    admin.router,
    tracking_router,
)
