"""Registration, login and e-mail lookup."""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Student
from app.schemas import (
    ClassSectionSelection,
    EmailCheckResponse,
    SessionInfo,
    StudentNumberSelection,
    StudentProfileCompletion,
    StudentRegister,
    Token,
)
from app.security import (
    create_access_token,
    get_current_account,
    hash_password,
    is_reserved_staff_email,
    verify_password,
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
    token = create_access_token({"sub": str(student.id), "ver": student.token_version})
    return Token(access_token=token, student_id=student.id, name=student.name,
                 is_teacher=student.role in ("teacher", "admin"), class_section=student.class_section,
                 role=student.role, is_admin=student.role == "admin", student_number=student.student_number)


def _session_for(account: Student) -> SessionInfo:
    return SessionInfo(student_id=account.id, name=account.name,
                       is_teacher=account.role in ("teacher", "admin"), class_section=account.class_section,
                       role=account.role, is_admin=account.role == "admin",
                       student_number=account.student_number)


async def find_login_account(db: AsyncSession, identifier: str) -> Optional[Student]:
    identifier = identifier.strip()
    if "@" in identifier:
        return await find_student_by_email(db, identifier)
    number = StudentNumberSelection.normalize_student_number(identifier)
    if not number or len(number) > 32 or not number.isascii() or not number.isdigit():
        return None
    return (await db.execute(select(Student).where(
        Student.student_number == number, Student.role == "student"))).scalar_one_or_none()


@router.post("/register", response_model=Token)
async def register(data: StudentRegister, db: AsyncSession = Depends(get_db)):
    email = data.email.strip().lower()

    # حساب الأستاذ لا يُنشأ من التسجيل العام: لا يوجد تحقق من ملكية البريد،
    # ومن يسجّل بريد الأستاذ أولاً كان سيحصل على صلاحياته.
    if is_reserved_staff_email(email):
        raise HTTPException(
            status_code=403,
            detail="هذا البريد مخصّص لحساب الأستاذ، ويُنشأ حسابه من قِبل إدارة المنصة",
        )

    if await find_student_by_email(db, email):
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجل مسبقاً")
    if (await db.execute(select(Student.id).where(Student.student_number == data.student_number))).first():
        raise HTTPException(status_code=409, detail="رقم الطالب مستخدم في حساب آخر")

    student = Student(
        name=data.name,
        email=email,
        password_hash=hash_password(data.password),
        year=1,
        class_section=data.class_section,
        student_number=data.student_number,
    )
    db.add(student)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="البريد الإلكتروني أو رقم الطالب مسجل مسبقًا") from None
    await db.refresh(student)
    return _token_for(student)


@router.get("/check-email", response_model=EmailCheckResponse)
async def check_email(email: str, db: AsyncSession = Depends(get_db)):
    # لا نُعيد الاسم حتى لا يُكشف اسم صاحب أي بريد لمن يعرف بريده
    return EmailCheckResponse(exists=await find_student_by_email(db, email) is not None)


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Form-encoded username accepts the e-mail or the student's unique number."""
    student = await find_login_account(db, form.username)

    if not student or not student.is_active or not verify_password(form.password, student.password_hash):
        raise HTTPException(status_code=401, detail="بيانات تسجيل الدخول غير صحيحة")

    await db.execute(
        update(Student).where(Student.id == student.id).values(last_login=datetime.utcnow())
    )
    await db.commit()
    return _token_for(student)


@router.get("/me", response_model=SessionInfo)
async def current_session(account: Student = Depends(get_current_account)):
    """Who the token belongs to. The frontend calls this to validate a stored login."""
    return _session_for(account)


@router.patch("/me/profile", response_model=SessionInfo)
async def complete_student_profile(
    data: StudentProfileCompletion, account: Student = Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    """Add a missing student number and section in one atomic, one-time operation."""
    if account.role != "student":
        raise HTTPException(status_code=403, detail="إكمال هذه البيانات مخصص للطلاب")
    section = data.class_section or account.class_section
    if section is None:
        raise HTTPException(status_code=422, detail="اختر شعبتك")
    if ((account.student_number is not None and account.student_number != data.student_number)
            or (account.class_section is not None and account.class_section != section)):
        raise HTTPException(status_code=409, detail="سبق حفظ بياناتك ولا يمكن تغييرها من هذه الصفحة")
    try:
        await db.execute(update(Student).where(
            Student.id == account.id, Student.role == "student",
            or_(Student.student_number.is_(None), Student.student_number == data.student_number),
            or_(Student.class_section.is_(None), Student.class_section == section),
        ).values(student_number=data.student_number, class_section=section, year=1))
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="رقم الطالب مستخدم في حساب آخر") from None
    await db.refresh(account)
    if account.student_number != data.student_number or account.class_section != section:
        raise HTTPException(status_code=409, detail="تغيرت بياناتك أثناء الحفظ. حدّث الصفحة وحاول مجددًا")
    return _session_for(account)


@router.patch("/me/section", response_model=SessionInfo)
async def choose_class_section(
    data: ClassSectionSelection,
    account: Student = Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    """Let an existing student choose their section once; never change another account."""
    if account.role != "student":
        raise HTTPException(status_code=403, detail="اختيار الشعبة مخصص للطلاب")

    # The condition also prevents competing requests from changing a choice.
    await db.execute(
        update(Student)
        .where(Student.id == account.id, Student.class_section.is_(None))
        .values(class_section=data.class_section, year=1)
    )
    await db.commit()
    await db.refresh(account)
    if account.class_section != data.class_section:
        raise HTTPException(status_code=409, detail="سبق تحديد شعبتك ولا يمكن تغييرها من هذه الصفحة")
    return _session_for(account)
