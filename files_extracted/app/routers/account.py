"""Self-service profile, password changes and one-time recovery links."""
import asyncio
import hashlib
import logging
import time
from collections import OrderedDict
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.models import Student
from app.routers.auth import _token_for, find_student_by_email
from app.security import create_access_token, get_current_account, hash_password, verify_password
from app.services.account_email import mail_ready, send_reset_email

router = APIRouter(prefix="/api/account", tags=["account"])
logger = logging.getLogger(__name__)
_requests: OrderedDict[str, list[float]] = OrderedDict()


class NewPassword(BaseModel):
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def fits_bcrypt(cls, value: str) -> str:
        if len(value.encode()) > 72:
            raise ValueError("كلمة المرور تتجاوز الحد المسموح")
        return value


class PasswordChange(NewPassword):
    current_password: str = Field(max_length=72)


class PasswordReset(NewPassword):
    token: str = Field(min_length=1, max_length=2048)


class ResetRequest(BaseModel):
    email: EmailStr


class ProfileChange(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    @field_validator("name", mode="before")
    @classmethod
    def trim_name(cls, value):
        return value.strip() if isinstance(value, str) else value


def limit_requests(request: Request, email: str | None = None) -> None:
    """Bounded per-process throttling; do not trust user-supplied forwarding headers."""
    now = time.monotonic()
    identifiers = [(f"ip:{request.client.host if request.client else 'unknown'}", 10)]
    if email is not None:
        identifiers.append((f"email:{email.lower()}", 3))
    keys = [(hashlib.sha256(value.encode()).hexdigest(), limit) for value, limit in identifiers]
    for key, limit in keys:
        recent = [stamp for stamp in _requests.get(key, []) if now - stamp < 900]
        if len(recent) >= limit:
            raise HTTPException(429, "طلبات كثيرة. حاول مجددًا بعد 15 دقيقة")
    for key, _ in keys:
        _requests[key] = [stamp for stamp in _requests.get(key, []) if now - stamp < 900] + [now]
        _requests.move_to_end(key)
    while len(_requests) > 10000:
        _requests.popitem(last=False)


@router.get("/me")
async def profile(account: Student = Depends(get_current_account)):
    return {"name": account.name, "email": account.email, "role": account.role,
            "student_number": account.student_number, "class_section": account.class_section}


@router.patch("/me")
async def update_profile(data: ProfileChange, account: Student = Depends(get_current_account),
                         db: AsyncSession = Depends(get_db)):
    await db.execute(update(Student).where(Student.id == account.id).values(name=data.name))
    await db.commit()
    await db.refresh(account)
    return _token_for(account)


async def replace_password(db: AsyncSession, account: Student, password: str, version: int):
    changed = await db.execute(update(Student).where(
        Student.id == account.id, Student.token_version == version, Student.is_active.is_(True)
    ).values(password_hash=hash_password(password), token_version=version + 1))
    if changed.rowcount != 1:
        await db.rollback()
        raise HTTPException(409, "تغير الحساب أو استُخدم الرابط. اطلب رابطًا جديدًا")
    await db.commit()
    await db.refresh(account)


@router.post("/password")
async def change_password(data: PasswordChange, account: Student = Depends(get_current_account),
                          db: AsyncSession = Depends(get_db)):
    if not verify_password(data.current_password, account.password_hash):
        raise HTTPException(400, "كلمة المرور الحالية غير صحيحة")
    await replace_password(db, account, data.password, account.token_version)
    return _token_for(account)


@router.post("/forgot-password")
async def forgot_password(data: ResetRequest, request: Request, db: AsyncSession = Depends(get_db)):
    if not mail_ready():
        raise HTTPException(503, "خدمة استعادة كلمة المرور غير مفعّلة بعد. تواصل مع إدارة المنصة")
    limit_requests(request, str(data.email))
    account = await find_student_by_email(db, str(data.email))
    if account and account.is_active:
        token = create_access_token(
            {"sub": str(account.id), "ver": account.token_version, "purpose": "password-reset"},
            timedelta(minutes=20),
        )
        try:
            await asyncio.to_thread(send_reset_email, account.email, token)
        except Exception:
            # Do not log credentials, mail addresses or links, or reveal account existence.
            logger.error("Password recovery mail delivery failed")
    return {"message": "إذا كان البريد مرتبطًا بحساب نشط، ستصلك رسالة استعادة كلمة المرور."}


@router.get("/recovery-status")
async def recovery_status():
    return {"enabled": mail_ready()}


@router.post("/reset-password")
async def reset_password(data: PasswordReset, request: Request, db: AsyncSession = Depends(get_db)):
    limit_requests(request)
    settings = get_settings()
    try:
        claims = jwt.decode(data.token, settings.secret_key, algorithms=[settings.algorithm])
        if claims.get("purpose") != "password-reset" or not isinstance(claims.get("ver"), int):
            raise ValueError
        account_id = int(claims["sub"])
    except (JWTError, ValueError, KeyError, TypeError):
        raise HTTPException(400, "رابط الاستعادة غير صالح أو انتهت صلاحيته") from None
    account = (await db.execute(select(Student).where(Student.id == account_id))).scalar_one_or_none()
    if not account or not account.is_active or account.token_version != claims["ver"]:
        raise HTTPException(400, "رابط الاستعادة غير صالح أو استُخدم مسبقًا")
    await replace_password(db, account, data.password, claims["ver"])
    return {"message": "تم تغيير كلمة المرور. سجّل الدخول بكلمة المرور الجديدة."}
