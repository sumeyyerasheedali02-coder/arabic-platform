from fastapi import HTTPException
from sqlalchemy import select, update

from app.models import Student
from app.services.staff import allowed_sections
from app.tracking.calculations import ACTIVITIES, overall_result, term_result, weekly_total
from app.tracking.models import (
    TrackingAudit,
    TrackingCycle,
    TrackingEntry,
    TrackingExam,
    TrackingTerm,
    TrackingWeek,
)


def record(row, fields):
    return {key: getattr(row, key) for key in fields}


async def cycle_for(db, account, cycle_id, *, staff=False):
    cycle = await db.get(TrackingCycle, cycle_id)
    if cycle is None:
        raise HTTPException(404, "السجل غير موجود")
    if account.role == "student":
        if staff or cycle.section != account.class_section:
            raise HTTPException(403, "غير مسموح بالوصول إلى هذه الشعبة")
    else:
        await allowed_sections(db, account, cycle.section)
    return cycle


async def roster(db, cycle):
    return list((await db.execute(select(Student).where(
        Student.role == "student", Student.is_active.is_(True),
        Student.class_section == cycle.section,
    ).order_by(Student.name, Student.id))).scalars())


async def claim_revision(db, cycle, expected):
    # Conditional UPDATE obtains a row lock on PostgreSQL before any mark is changed.
    # A competing teacher cannot overwrite a saved revision, even on another tab.
    result = await db.execute(update(TrackingCycle).where(
        TrackingCycle.id == cycle.id, TrackingCycle.revision == expected,
    ).values(revision=TrackingCycle.revision + 1).execution_options(synchronize_session=False))
    if result.rowcount != 1:
        raise HTTPException(409, "عدّل أستاذ آخر هذا السجل. حدّث البيانات قبل الحفظ")
    await db.refresh(cycle)


def validate_students(entries, students):
    ids = [entry.student_id for entry in entries]
    if len(ids) != len(set(ids)):
        raise HTTPException(422, "يوجد طالب مكرر في الطلب")
    if not set(ids).issubset({student.id for student in students}):
        raise HTTPException(403, "لا يمكنك إدخال درجات لطالب خارج شُعبتك")


def audit(db, cycle, account, action, details):
    db.add(TrackingAudit(cycle_id=cycle.id, actor_id=account.id, action=action, details=details))


async def snapshot(db, cycle, students):
    weeks = (await db.execute(select(TrackingWeek).where(
        TrackingWeek.cycle_id == cycle.id).order_by(TrackingWeek.number))).scalars().all()
    terms = (await db.execute(select(TrackingTerm).where(
        TrackingTerm.cycle_id == cycle.id).order_by(TrackingTerm.number))).scalars().all()
    ids = [s.id for s in students]
    entries = (await db.execute(select(TrackingEntry).join(TrackingWeek).where(
        TrackingWeek.cycle_id == cycle.id, TrackingEntry.student_id.in_(ids)))).scalars().all()
    exams = (await db.execute(select(TrackingExam).join(TrackingTerm).where(
        TrackingTerm.cycle_id == cycle.id, TrackingExam.student_id.in_(ids)))).scalars().all()
    return {
        "cycle": record(cycle, ("id", "academic_year", "section", "revision", "final_published")),
        "students": [record(s, ("id", "name", "student_number", "class_section")) for s in students],
        "weeks": [record(w, ("id", "number", "starts_on", "published")) for w in weeks],
        "terms": [record(t, ("id", "number", "first_week", "last_week", "published")) for t in terms],
        "entries": [record(e, ("student_id", "week_id", *ACTIVITIES, "note")) for e in entries],
        "exams": [record(e, ("student_id", "term_id", "score")) for e in exams],
    }


async def invalidate_terms(db, cycle, week_number=None):
    query = update(TrackingTerm).where(TrackingTerm.cycle_id == cycle.id)
    if week_number is not None:
        query = query.where(TrackingTerm.first_week <= week_number, TrackingTerm.last_week >= week_number)
    await db.execute(query.values(published=False))
    cycle.final_published = False


def require_week_complete(data, week_id):
    values = {e["student_id"]: e for e in data["entries"] if e["week_id"] == week_id}
    if not data["students"] or any(weekly_total(values.get(s["id"])) is None for s in data["students"]):
        raise HTTPException(422, "أكمل الفعاليات الأربع لجميع طلاب الشعبة قبل النشر")


def results_for(data, student_id, *, published_only=False):
    entries = {e["week_id"]: e for e in data["entries"] if e["student_id"] == student_id}
    exams = {e["term_id"]: e["score"] for e in data["exams"] if e["student_id"] == student_id}
    terms = {t["number"]: t for t in data["terms"]}
    results = [term_result(terms.get(n), data["weeks"], entries,
                           exams.get(terms[n]["id"]) if n in terms else None,
                           published_only=published_only) for n in (1, 2)]
    return {"terms": results, "overall": overall_result(results)}


def require_term_complete(data, number):
    if not data["students"]:
        raise HTTPException(422, "لا يوجد طلاب في هذه الشعبة")
    for student in data["students"]:
        result = results_for(data, student["id"], published_only=False)["terms"][number - 1]
        if result is None or result["total"] is None:
            raise HTTPException(422, "أكمل كل أسابيع الفصل وعلامة الامتحان لجميع الطلاب قبل النشر")
    term = next(t for t in data["terms"] if t["number"] == number)
    if any(not w["published"] for w in data["weeks"]
           if term["first_week"] <= w["number"] <= term["last_week"]):
        raise HTTPException(422, "انشر أسابيع الفصل قبل نشر نتيجته")
