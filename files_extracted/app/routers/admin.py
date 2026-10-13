"""Only administrators may manage teachers and correct student sections."""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.config import ADMIN_EMAIL
from app.database import get_db
from app.models import AdminAudit, Student, TeacherSection
from app.schemas import ClassSectionSelection, TeacherCreate, TeacherInfo, TeacherUpdate
from app.security import get_current_admin, hash_password
from app.services.staff import audit, teacher_infos

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/audit")
async def audit_log(
    offset: int = Query(0, ge=0), limit: int = Query(25, ge=1, le=100),
    action: Literal["teacher_created", "teacher_updated", "student_section_changed"] | None = None,
    admin: Student = Depends(get_current_admin), db: AsyncSession = Depends(get_db),
):
    actor, target = aliased(Student), aliased(Student)
    query = select(
        AdminAudit.id, AdminAudit.action, AdminAudit.details, AdminAudit.created_at,
        actor.name.label("actor_name"), target.id.label("target_id"),
        target.name.label("target_name"), target.role.label("target_role"),
    ).join(actor, actor.id == AdminAudit.actor_id).join(target, target.id == AdminAudit.target_id)
    count = select(func.count(AdminAudit.id))
    if action is not None:
        query = query.where(AdminAudit.action == action)
        count = count.where(AdminAudit.action == action)
    total = (await db.execute(count)).scalar()
    rows = (await db.execute(query.order_by(AdminAudit.created_at.desc(), AdminAudit.id.desc())
                             .offset(offset).limit(limit))).mappings().all()
    safe_keys = {"sections", "previous_sections", "is_active", "password_reset",
                 "previous_section", "class_section"}
    return {"total": total, "items": [
        dict(row, details={key: value for key, value in row["details"].items() if key in safe_keys})
        for row in rows
    ]}


@router.get("/teachers", response_model=list[TeacherInfo])
async def list_teachers(
    admin: Student = Depends(get_current_admin), db: AsyncSession = Depends(get_db),
):
    return await teacher_infos(db)


@router.post("/teachers", response_model=TeacherInfo, status_code=201)
async def create_teacher(
    data: TeacherCreate, admin: Student = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    email = str(data.email).strip().lower()
    if email == ADMIN_EMAIL:
        raise HTTPException(status_code=409, detail="هذا البريد مخصص لمدير المنصة")
    if (await db.execute(select(Student.id).where(func.lower(Student.email) == email))).first():
        raise HTTPException(status_code=409, detail="البريد مسجل مسبقًا؛ استخدم بريدًا آخر لحساب الأستاذ")
    teacher = Student(name=data.name, email=email, password_hash=hash_password(data.password),
                      role="teacher", year=1)
    db.add(teacher)
    try:
        await db.flush()
        sections = sorted(set(data.sections))
        db.add_all([TeacherSection(teacher_id=teacher.id, class_section=s) for s in sections])
        audit(db, admin, teacher, "teacher_created", {"sections": sections})
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="البريد مسجل مسبقًا") from None
    return TeacherInfo(id=teacher.id, name=teacher.name, email=teacher.email,
                       sections=sections, is_active=True)


@router.patch("/teachers/{teacher_id}", response_model=TeacherInfo)
async def update_teacher(
    teacher_id: int, data: TeacherUpdate, admin: Student = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    teacher = (await db.execute(
        select(Student).where(Student.id == teacher_id, Student.role == "teacher").with_for_update()
    )).scalar_one_or_none()
    if teacher is None:
        raise HTTPException(status_code=404, detail="حساب الأستاذ غير موجود")
    sections = sorted(set(data.sections))
    if data.is_active and not sections:
        raise HTTPException(status_code=422, detail="يجب إسناد شعبة واحدة على الأقل للأستاذ النشط")
    before = list((await db.execute(select(TeacherSection.class_section)
                                   .where(TeacherSection.teacher_id == teacher_id))).scalars())
    await db.execute(delete(TeacherSection).where(TeacherSection.teacher_id == teacher_id))
    db.add_all([TeacherSection(teacher_id=teacher_id, class_section=s) for s in sections])
    if teacher.is_active != data.is_active or data.password is not None:
        teacher.token_version += 1
    teacher.is_active = data.is_active
    if data.password is not None:
        teacher.password_hash = hash_password(data.password)
    audit(db, admin, teacher, "teacher_updated", {
        "previous_sections": sorted(before), "sections": sections,
        "is_active": data.is_active, "password_reset": data.password is not None,
    })
    await db.commit()
    return TeacherInfo(id=teacher.id, name=teacher.name, email=teacher.email,
                       sections=sections, is_active=teacher.is_active)


@router.patch("/students/{student_id}/section")
async def correct_section(
    student_id: int, data: ClassSectionSelection, admin: Student = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    student = (await db.execute(select(Student).where(
        Student.id == student_id, Student.role == "student").with_for_update())).scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail="حساب الطالب غير موجود")
    previous = student.class_section
    student.class_section = data.class_section
    student.year = 1
    audit(db, admin, student, "student_section_changed",
          {"previous_section": previous, "class_section": data.class_section})
    await db.commit()
    return {"student_id": student.id, "class_section": student.class_section}
