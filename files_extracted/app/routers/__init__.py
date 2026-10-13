"""HTTP routers, one module per feature. All paths live under /api."""
from app.routers import admin, auth, chat, content, exercises, progress, srs, teacher

ALL_ROUTERS = (
    auth.router,
    content.router,
    exercises.router,
    progress.router,
    srs.router,
    chat.router,
    teacher.router,
    admin.router,
)
