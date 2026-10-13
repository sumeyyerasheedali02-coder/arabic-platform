"""Registration, login and e-mail lookup."""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Student
from app.schemas import EmailCheckResponse, SessionInfo, StudentRegister, Token
from app.security import (
    create_access_token, get_current_account, hash_password, is_teacher_email, verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


async def find_student_by_email(db: AsyncSession, email: str) -> Optional[Student]:
    """Addresses are compared without regard to letter case."""
    result = await db.execute(
        select(Student)
        .where(func.lower(Student.email) == email.strip().lower())
        .order_by(Student.id)
        .limit(1)
    )
    return result.scalar_one_or_none()


def _token_for(student: Student) -> Token:
    # python-jose requires the `sub` claim to be a string.
    token = create_access_token({"sub": str(student.id)})
    return Token(access_token=token, student_id=student.id, name=student.name,
                 is_teacher=is_teacher_email(student.email))


@router.post("/register", response_model=Token)
async def register(data: StudentRegister, db: AsyncSession = Depends(get_db)):
    email = data.email.strip().lower()

    # حساب الأستاذ لا يُنشأ من التسجيل العام: لا يوجد تحقق من ملكية البريد،
    # ومن يسجّل بريد الأستاذ أولاً كان سيحصل على صلاحياته.
    if is_teacher_email(email):
        raise HTTPException(
            status_code=403,
            detail="هذا البريد مخصّص لحساب الأستاذ، ويُنشأ حسابه من قِبل إدارة المنصة",
        )

    if await find_student_by_email(db, email):
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجل مسبقاً")

    student = Student(
        name=data.name,
        email=email,
        password_hash=hash_password(data.password),
        year=data.year,
    )
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return _token_for(student)


@router.get("/check-email", response_model=EmailCheckResponse)
async def check_email(email: str, db: AsyncSession = Depends(get_db)):
    # لا نُعيد الاسم حتى لا يُكشف اسم صاحب أي بريد لمن يعرف بريده
    return EmailCheckResponse(exists=await find_student_by_email(db, email) is not None)


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """OAuth2 password flow: form-encoded `username` (the e-mail) and `password`."""
    student = await find_student_by_email(db, form.username)

    if not student or not verify_password(form.password, student.password_hash):
        raise HTTPException(status_code=401, detail="بيانات تسجيل الدخول غير صحيحة")

    await db.execute(
        update(Student).where(Student.id == student.id).values(last_login=datetime.utcnow())
    )
    await db.commit()
    return _token_for(student)


@router.get("/me", response_model=SessionInfo)
async def current_session(account: Student = Depends(get_current_account)):
    """Who the token belongs to. The frontend calls this to validate a stored login."""
    return SessionInfo(student_id=account.id, name=account.name,
                       is_teacher=is_teacher_email(account.email))
