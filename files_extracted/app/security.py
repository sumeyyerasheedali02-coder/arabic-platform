"""Password hashing, JWT handling and the authentication dependencies."""
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.models import Student

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def is_teacher_email(email: str) -> bool:
    """Teachers are the accounts whose address is listed in TEACHER_EMAILS."""
    return settings.is_teacher_email(email)


# passlib is deliberately not used: passlib 1.7.4 breaks with bcrypt >= 4.
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except ValueError:
        # A stored hash that is not bcrypt, or (bcrypt >= 5) a password over 72 bytes
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def get_current_account(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Student:
    """Return the account the token belongs to, or answer 401.

    The token must be valid, unexpired, carry a numeric subject, and that
    account must still exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="بيانات الاعتماد غير صالحة",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        # python-jose requires `sub` to be a string; ids are stored as str(id).
        student_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise credentials_exception

    student = (await db.execute(select(Student).where(Student.id == student_id))).scalar_one_or_none()
    if student is None:
        raise credentials_exception
    return student


async def get_current_student(account: Student = Depends(get_current_account)) -> int:
    """The id of the logged-in student (401 when not logged in)."""
    return account.id


async def get_current_teacher(account: Student = Depends(get_current_account)) -> int:
    """Like get_current_student, but answers 403 unless the account is a teacher."""
    if not is_teacher_email(account.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="هذه الصفحة مخصصة للأستاذ فقط",
        )
    return account.id
