"""Scoped grade APIs for the separately deployed tracking frontend."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.models import Student
from app.security import get_current_account, get_current_teacher
from app.services.staff import allowed_sections
from app.tracking import service as svc
from app.tracking.calculations import weekly_total
from app.tracking.models import (
    TrackingAudit,
    TrackingCycle,
    TrackingEntry,
    TrackingExam,
    TrackingTerm,
    TrackingWeek,
)
from app.tracking.schemas import CycleCreate, Publication, TermSave, WeekCreate, WeekSave

router = APIRouter(prefix="/api/tracking", tags=["tracking"])
staff = [Depends(get_current_teacher)]


@router.get("/site")
async def tracking_site():
    """Public navigation metadata only; grades still require an authenticated account."""
    return {"site_url": get_settings().tracking_site_url or None}


@router.get("/cycles")
async def cycles(account: Student = Depends(get_current_account), db: AsyncSession = Depends(get_db)):
    sections = ([account.class_section] if account.role == "student"
                else await allowed_sections(db, account))
    rows = (await db.execute(select(TrackingCycle).where(TrackingCycle.section.in_(sections))
                            .order_by(TrackingCycle.academic_year.desc(), TrackingCycle.section))).scalars()
    return {"sections": [s for s in sections if s], "cycles": [svc.record(c, (
        "id", "academic_year", "section", "revision", "final_published")) for c in rows]}


@router.post("/cycles", dependencies=staff, status_code=201)
async def create_cycle(data: CycleCreate, account: Student = Depends(get_current_account),
                       db: AsyncSession = Depends(get_db)):
    await allowed_sections(db, account, data.section)
    cycle = TrackingCycle(**data.model_dump())
    db.add(cycle)
    try:
        await db.flush()
        svc.audit(db, cycle, account, "cycle_created", data.model_dump())
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, "سجل الشعبة لهذا العام موجود بالفعل") from None
    return svc.record(cycle, ("id", "academic_year", "section", "revision", "final_published"))


@router.get("/cycles/{cycle_id}/state", dependencies=staff)
async def state(cycle_id: int, account: Student = Depends(get_current_account),
                db: AsyncSession = Depends(get_db)):
    cycle = await svc.cycle_for(db, account, cycle_id, staff=True)
    data = await svc.snapshot(db, cycle, await svc.roster(db, cycle))
    logs = (await db.execute(select(TrackingAudit, Student.name).join(
        Student, Student.id == TrackingAudit.actor_id).where(TrackingAudit.cycle_id == cycle_id)
        .order_by(TrackingAudit.id.desc()).limit(30))).all()
    data["audit"] = [{"id": a.id, "actor": name, "action": a.action,
                      "created_at": a.created_at} for a, name in logs]
    data["results"] = {s["id"]: svc.results_for(data, s["id"]) for s in data["students"]}
    return data


@router.post("/cycles/{cycle_id}/weeks", dependencies=staff, status_code=201)
async def add_week(cycle_id: int, data: WeekCreate, account: Student = Depends(get_current_account),
                   db: AsyncSession = Depends(get_db)):
    cycle = await svc.cycle_for(db, account, cycle_id, staff=True)
    await svc.claim_revision(db, cycle, data.revision)
    if (await db.execute(select(TrackingWeek.id).where(
        TrackingWeek.cycle_id == cycle.id, TrackingWeek.number == data.number))).first():
        raise HTTPException(409, "رقم الأسبوع موجود بالفعل")
    week = TrackingWeek(cycle_id=cycle.id, number=data.number, starts_on=data.starts_on)
    db.add(week)
    await svc.invalidate_terms(db, cycle, data.number)
    svc.audit(db, cycle, account, "week_created", data.model_dump(mode="json"))
    await db.commit()
    return {"revision": cycle.revision, "week_id": week.id}


async def week_for(db, cycle, week_id):
    week = await db.get(TrackingWeek, week_id)
    if week is None or week.cycle_id != cycle.id:
        raise HTTPException(404, "الأسبوع غير موجود")
    return week


@router.put("/cycles/{cycle_id}/weeks/{week_id}", dependencies=staff)
async def save_week(cycle_id: int, week_id: int, data: WeekSave,
                    account: Student = Depends(get_current_account), db: AsyncSession = Depends(get_db)):
    cycle = await svc.cycle_for(db, account, cycle_id, staff=True)
    await svc.claim_revision(db, cycle, data.revision)
    week = await week_for(db, cycle, week_id)
    students = await svc.roster(db, cycle)
    svc.validate_students(data.entries, students)
    existing = {e.student_id: e for e in (await db.execute(select(TrackingEntry).where(
        TrackingEntry.week_id == week.id))).scalars()}
    changes = []
    for entry in data.entries:
        values = entry.model_dump(exclude={"student_id"})
        row = existing.get(entry.student_id)
        before = svc.record(row, values) if row is not None else None
        if row is None:
            row = TrackingEntry(week_id=week.id, student_id=entry.student_id)
            db.add(row)
        for key, value in values.items():
            setattr(row, key, value)
        changes.append({"student_id": entry.student_id, "before": before, "after": values})
    week.published = data.publish
    await svc.invalidate_terms(db, cycle, week.number)
    await db.flush()
    if data.publish:
        svc.require_week_complete(await svc.snapshot(db, cycle, students), week.id)
    svc.audit(db, cycle, account, "week_saved", {
        "week": week.number, "published": data.publish, "changes": changes})
    await db.commit()
    return {"revision": cycle.revision}


@router.patch("/cycles/{cycle_id}/weeks/{week_id}/publication", dependencies=staff)
async def publish_week(cycle_id: int, week_id: int, data: Publication,
                       account: Student = Depends(get_current_account), db: AsyncSession = Depends(get_db)):
    cycle = await svc.cycle_for(db, account, cycle_id, staff=True)
    await svc.claim_revision(db, cycle, data.revision)
    week = await week_for(db, cycle, week_id)
    if data.published:
        svc.require_week_complete(await svc.snapshot(db, cycle, await svc.roster(db, cycle)), week.id)
    week.published = data.published
    await svc.invalidate_terms(db, cycle, week.number)
    svc.audit(db, cycle, account, "week_publication", {"week": week.number, "published": data.published})
    await db.commit()
    return {"revision": cycle.revision}


@router.put("/cycles/{cycle_id}/terms/{number}", dependencies=staff)
async def save_term(cycle_id: int, number: int, data: TermSave,
                    account: Student = Depends(get_current_account), db: AsyncSession = Depends(get_db)):
    if number not in (1, 2):
        raise HTTPException(422, "رقم الفصل يجب أن يكون 1 أو 2")
    cycle = await svc.cycle_for(db, account, cycle_id, staff=True)
    await svc.claim_revision(db, cycle, data.revision)
    students = await svc.roster(db, cycle)
    svc.validate_students(data.entries, students)
    other = (await db.execute(select(TrackingTerm).where(
        TrackingTerm.cycle_id == cycle.id, TrackingTerm.number != number))).scalar_one_or_none()
    if other and data.first_week <= other.last_week and data.last_week >= other.first_week:
        raise HTTPException(422, "لا يمكن أن تتداخل أسابيع الفصلين")
    term = (await db.execute(select(TrackingTerm).where(
        TrackingTerm.cycle_id == cycle.id, TrackingTerm.number == number))).scalar_one_or_none()
    if term is None:
        term = TrackingTerm(cycle_id=cycle.id, number=number)
        db.add(term)
    term.first_week, term.last_week, term.published = data.first_week, data.last_week, data.publish
    cycle.final_published = False
    await db.flush()
    existing = {e.student_id: e for e in (await db.execute(select(TrackingExam).where(
        TrackingExam.term_id == term.id))).scalars()}
    changes = []
    for entry in data.entries:
        row = existing.get(entry.student_id)
        before = row.score if row else None
        if row is None:
            row = TrackingExam(term_id=term.id, student_id=entry.student_id)
            db.add(row)
        row.score = entry.score
        changes.append({"student_id": entry.student_id, "before": before, "after": entry.score})
    await db.flush()
    if data.publish:
        svc.require_term_complete(await svc.snapshot(db, cycle, students), number)
    svc.audit(db, cycle, account, "term_saved", {
        "number": number, "first_week": data.first_week, "last_week": data.last_week,
        "published": data.publish, "changes": changes})
    await db.commit()
    return {"revision": cycle.revision}


@router.patch("/cycles/{cycle_id}/final-publication", dependencies=staff)
async def publish_final(cycle_id: int, data: Publication,
                        account: Student = Depends(get_current_account), db: AsyncSession = Depends(get_db)):
    cycle = await svc.cycle_for(db, account, cycle_id, staff=True)
    await svc.claim_revision(db, cycle, data.revision)
    snapshot = await svc.snapshot(db, cycle, await svc.roster(db, cycle))
    if data.published:
        for number in (1, 2):
            svc.require_term_complete(snapshot, number)
        if len(snapshot["terms"]) != 2 or not all(t["published"] for t in snapshot["terms"]):
            raise HTTPException(422, "انشر نتيجة الفصلين أولاً")
    cycle.final_published = data.published
    svc.audit(db, cycle, account, "final_publication", {"published": data.published})
    await db.commit()
    return {"revision": cycle.revision}


@router.get("/cycles/{cycle_id}/me")
async def my_results(cycle_id: int, account: Student = Depends(get_current_account),
                     db: AsyncSession = Depends(get_db)):
    if account.role != "student":
        raise HTTPException(403, "هذه الصفحة مخصصة للطالب")
    cycle = await svc.cycle_for(db, account, cycle_id)
    data = await svc.snapshot(db, cycle, [account])
    results = svc.results_for(data, account.id, published_only=True)
    published = {w["id"] for w in data["weeks"] if w["published"]}
    data["weeks"] = [w for w in data["weeks"] if w["id"] in published]
    data["entries"] = [e for e in data["entries"] if e["week_id"] in published
                       and weekly_total(e) is not None]
    # Never return drafts/exam values/other students through the student's API.
    del data["terms"], data["exams"]
    if not cycle.final_published:
        results["overall"] = None
    data["results"] = results
    return data
