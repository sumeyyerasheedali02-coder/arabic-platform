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
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def get_current_student(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> int:
    """Return the id of the logged-in student, or answer 401."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="بيانات الاعتماد غير صالحة",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        # python-jose requires `sub` to be a string; ids are stored as str(id).
        student_id: int = int(sub)
    except JWTError:
        raise credentials_exception
    return student_id


async def get_current_teacher(
    student_id: int = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> int:
    """Like get_current_student, but answers 403 unless the account is a teacher."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student or not is_teacher_email(student.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="هذه الصفحة مخصصة للأستاذ فقط",
        )
    return student_id
