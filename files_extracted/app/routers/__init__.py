"""HTTP routers, one module per feature. All paths live under /api."""
from app.routers import auth, chat, content, exercises, progress, srs, teacher

ALL_ROUTERS = (
    auth.router,
    content.router,
    exercises.router,
    progress.router,
    srs.router,
    chat.router,
    teacher.router,
)
