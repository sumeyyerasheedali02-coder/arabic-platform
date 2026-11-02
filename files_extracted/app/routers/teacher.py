"""Teacher reports restricted to assigned sections; admins see all students."""
import secrets

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Exercise, ExerciseAnswer, Student, TeacherSection
from app.schemas import ClassSection, SectionInfo, StudentSummary, UnitStats
from app.security import get_current_account, get_current_teacher, hash_password
from app.services import reporting
from app.services.staff import allowed_sections, audit, authorized_student

router = APIRouter(prefix="/api/teacher", tags=["teacher"],
                   dependencies=[Depends(get_current_teacher)])


@router.get("/activity")
async def recent_activity(
    section: ClassSection | None = None, limit: int = Query(10, ge=1, le=50),
    account: Student = Depends(get_current_account), db: AsyncSession = Depends(get_db),
):
    allowed = await allowed_sections(db, account, section)
    scope = reporting.student_scope(None if account.role == "admin" and section is None else allowed)
    rows = (await db.execute(select(
        ExerciseAnswer.id, ExerciseAnswer.student_id, Student.name,
        Student.class_section, Exercise.question_ar, ExerciseAnswer.is_correct,
        ExerciseAnswer.answered_at,
    ).join(Student, Student.id == ExerciseAnswer.student_id)
      .join(Exercise, Exercise.id == ExerciseAnswer.exercise_id)
      .where(ExerciseAnswer.student_id.in_(scope))
      .order_by(ExerciseAnswer.answered_at.desc(), ExerciseAnswer.id.desc()).limit(limit))).mappings().all()
    return [dict(row) for row in rows]


@router.get("/sections", response_model=list[SectionInfo])
async def sections(
    account: Student = Depends(get_current_account), db: AsyncSession = Depends(get_db),
):
    allowed = await allowed_sections(db, account)
    students = dict((await db.execute(select(Student.class_section, func.count(Student.id))
                                     .where(Student.role == "student")
                                     .group_by(Student.class_section))).all())
    teachers = dict((await db.execute(select(TeacherSection.class_section, func.count())
                                     .join(Student, Student.id == TeacherSection.teacher_id)
                                     .where(Student.role == "teacher", Student.is_active.is_(True))
                                     .group_by(TeacherSection.class_section))).all())
    return [SectionInfo(class_section=s, students_count=students.get(s, 0),
                        teachers_count=teachers.get(s, 0)) for s in allowed]


@router.get("/students", response_model=list[StudentSummary])
async def students(
    section: ClassSection | None = None, account: Student = Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    allowed = await allowed_sections(db, account, section)
    return await reporting.student_summaries(
        db, None if account.role == "admin" and section is None else allowed)


@router.get("/units/stats", response_model=list[UnitStats])
async def unit_stats(
    section: ClassSection | None = None, account: Student = Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    allowed = await allowed_sections(db, account, section)
    return await reporting.unit_stats(
        db, None if account.role == "admin" and section is None else allowed)


@router.get("/students/{student_id}")
async def student_details(
    student_id: int, account: Student = Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    await authorized_student(db, account, student_id)
    return await reporting.student_details(db, student_id)


# No 0/O, 1/l/I: the password is read aloud or copied by hand to the student.
_TEMPORARY_ALPHABET = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
TEMPORARY_PASSWORD_LENGTH = 10


@router.post("/students/{student_id}/reset-password")
async def reset_student_password(
    student_id: int, response: Response, account: Student = Depends(get_current_account),
    db: AsyncSession = Depends(get_db),
):
    """Give a student who forgot the password a temporary one (shown once to the teacher).

    Allowed for the student's own teachers and for admins. Every session the student
    still has is revoked, and the audit trail records who did it, never the password.
    """
    student = await authorized_student(db, account, student_id)
    temporary = "".join(secrets.choice(_TEMPORARY_ALPHABET) for _ in range(TEMPORARY_PASSWORD_LENGTH))
    await db.execute(update(Student).where(Student.id == student.id).values(
        password_hash=hash_password(temporary), token_version=Student.token_version + 1))
    audit(db, account, student, "student_password_reset", {"password_reset": True})
    await db.commit()
    response.headers["Cache-Control"] = "no-store"
    return {"temporary_password": temporary}
