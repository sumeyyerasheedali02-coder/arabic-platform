"""Section access checks and staff account administration."""
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAudit, Student, TeacherSection
from app.schemas import TeacherInfo

SECTIONS = ("A", "B", "C", "D")


async def allowed_sections(db: AsyncSession, account: Student, section: str | None = None) -> list[str]:
    if account.role == "admin":
        allowed = list(SECTIONS)
    else:
        allowed = list((await db.execute(
            select(TeacherSection.class_section)
            .where(TeacherSection.teacher_id == account.id)
            .order_by(TeacherSection.class_section)
        )).scalars())
    if section is not None:
        if section not in allowed:
            raise HTTPException(status_code=403, detail="هذه الشعبة غير مسندة إليك")
        return [section]
    return allowed


async def authorized_student(db: AsyncSession, account: Student, student_id: int) -> Student:
    sections = await allowed_sections(db, account)
    query = select(Student).where(Student.id == student_id, Student.role == "student")
    if account.role != "admin":
        query = query.where(Student.class_section.in_(sections))
    student = (await db.execute(query)).scalar_one_or_none()
    if student is None:
        # Same response for a missing student and a student outside this teacher's scope.
        raise HTTPException(status_code=404, detail="الطالب غير موجود ضمن الطلاب المسؤول عنهم")
    return student


async def teacher_infos(db: AsyncSession) -> list[TeacherInfo]:
    teachers = (await db.execute(
        select(Student).where(Student.role == "teacher").order_by(Student.name, Student.id)
    )).scalars().all()
    assignments: dict[int, list[str]] = {}
    for teacher_id, section in (await db.execute(
        select(TeacherSection.teacher_id, TeacherSection.class_section)
        .order_by(TeacherSection.class_section)
    )).all():
        assignments.setdefault(teacher_id, []).append(section)
    return [TeacherInfo(id=t.id, name=t.name, email=t.email,
                        is_active=t.is_active, sections=assignments.get(t.id, [])) for t in teachers]


def audit(db: AsyncSession, actor: Student, target: Student, action: str, details: dict) -> None:
    # Never store passwords, password hashes, or tokens in the audit trail.
    db.add(AdminAudit(actor_id=actor.id, target_id=target.id, action=action, details=details))
