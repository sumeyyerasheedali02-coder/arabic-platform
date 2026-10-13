from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
import os
import secrets
from dotenv import load_dotenv
from database import get_db, Student

load_dotenv()

logger = logging.getLogger(__name__)

# Values that are public knowledge (old code default, .env.example placeholder).
# Anyone can forge a login token for any account if one of them signs the tokens.
INSECURE_SECRET_KEYS = {"", "change-this-secret", "your-secret-key-here"}


def load_secret_key() -> str:
    """Return the JWT signing key, never a publicly known one.

    Without a real SECRET_KEY the process signs with a random key that lives
    only in memory: the API stays usable and safe, but every restart logs
    everyone out. Set ENVIRONMENT=production to refuse to start instead.
    """
    key = os.getenv("SECRET_KEY", "").strip()
    if key not in INSECURE_SECRET_KEYS:
        return key
    if os.getenv("ENVIRONMENT", "").strip().lower() == "production":
        raise RuntimeError(
            "SECRET_KEY is missing or is a placeholder. Generate one with "
            "`python -c \"import secrets; print(secrets.token_urlsafe(48))\"` "
            "and set it in the environment.")
    logger.warning(
        "SECRET_KEY is missing or is a placeholder: using a temporary random key. "
        "All logins become invalid when the server restarts. Set SECRET_KEY to fix this.")
    return secrets.token_urlsafe(48)


SECRET_KEY = load_secret_key()
ALGORITHM  = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10080))

# بريد الأساتذة مفصول بفواصل — وحدهم يرون بيانات الطلاب الآخرين
TEACHER_EMAILS = {
    e.strip().lower() for e in os.getenv("TEACHER_EMAILS", "").split(",") if e.strip()
}


def is_teacher_email(email: str) -> bool:
    return (email or "").strip().lower() in TEACHER_EMAILS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_student(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="بيانات الاعتماد غير صالحة",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        student_id: int = int(sub)
    except JWTError:
        raise credentials_exception
    return student_id


async def get_current_teacher(
    student_id: int = Depends(get_current_student),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student or not is_teacher_email(student.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="هذه الصفحة مخصصة للأستاذ فقط",
        )
    return student_id
