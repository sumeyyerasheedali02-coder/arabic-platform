"""
منصة العربية بين يديك — Arabic Learning Platform
FastAPI Backend — v1.0
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, update
from datetime import datetime, date
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

from google import genai
_genai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

from database import (
    get_db, init_db,
    Unit, Lesson, Vocabulary, Dialogue, DialogueLine,
    Exercise, ExerciseAnswer, Student, StudentProgress, SRSCard, AISession
)
from auth import hash_password, verify_password, create_access_token, get_current_student
from schemas import (
    StudentRegister, Token, EmailCheckResponse, UnitOut, LessonOut, VocabularyOut,
    DialogueOut, ExerciseOut, AnswerSubmit, AnswerResult,
    ProgressOut, ChatRequest, ChatResponse, SRSReview, SRSCardOut,
    StudentSummary, UnitStats
)
from srs import sm2, get_due_cards

# ─────────────────────────────────────────
#  إنشاء التطبيق
# ─────────────────────────────────────────
app = FastAPI(
    title="منصة العربية بين يديك",
    description="نظام تعلم اللغة العربية للطلاب الأتراك في كلية الإلهيات",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://arabic-platform-flame.vercel.app","http://localhost:5173","http://localhost:8003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await init_db()


# ─────────────────────────────────────────
#  الصفحة الرئيسية
# ─────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "message": "مرحباً بك في منصة العربية بين يديك",
        "version": "1.0.0",
        "docs": "/docs"
    }


# ═══════════════════════════════════════════
#  المصادقة (Auth)
# ═══════════════════════════════════════════
@app.post("/api/auth/register", response_model=Token)
async def register(data: StudentRegister, db: AsyncSession = Depends(get_db)):
    # التحقق من عدم وجود الإيميل مسبقاً
    result = await db.execute(select(Student).where(Student.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مسجل مسبقاً")

    student = Student(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        year=data.year,
    )
    db.add(student)
    await db.commit()
    await db.refresh(student)

    token = create_access_token({"sub": str(student.id)})
    return Token(access_token=token, student_id=student.id, name=student.name)


@app.get("/api/auth/check-email", response_model=EmailCheckResponse)
async def check_email(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.email == email))
    student = result.scalar_one_or_none()
    if student:
        return EmailCheckResponse(exists=True, name=student.name)
    return EmailCheckResponse(exists=False)


@app.post("/api/auth/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.email == form.username))
    student = result.scalar_one_or_none()

    if not student or not verify_password(form.password, student.password_hash):
        raise HTTPException(status_code=401, detail="بيانات تسجيل الدخول غير صحيحة")

    await db.execute(
        update(Student).where(Student.id == student.id).values(last_login=datetime.utcnow())
    )
    await db.commit()

    token = create_access_token({"sub": str(student.id)})
    return Token(access_token=token, student_id=student.id, name=student.name)


# ═══════════════════════════════════════════
#  الوحدات (Units)
# ═══════════════════════════════════════════
@app.get("/api/units", response_model=List[UnitOut])
async def get_units(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit).order_by(Unit.unit_number))
    return result.scalars().all()


@app.get("/api/units/{unit_id}", response_model=UnitOut)
async def get_unit(unit_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Unit).where(Unit.id == unit_id))
    unit = result.scalar_one_or_none()
    if not unit:
        raise HTTPException(status_code=404, detail="الوحدة غير موجودة")
    return unit


# ═══════════════════════════════════════════
#  الدروس (Lessons)
# ═══════════════════════════════════════════
@app.get("/api/units/{unit_id}/lessons", response_model=List[LessonOut])
async def get_lessons(unit_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson)
        .where(Lesson.unit_id == unit_id)
        .order_by(Lesson.lesson_number)
    )
    return result.scalars().all()


@app.get("/api/lessons/{lesson_id}", response_model=LessonOut)
async def get_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="الدرس غير موجود")
    return lesson


# ═══════════════════════════════════════════
#  المفردات (Vocabulary)
# ═══════════════════════════════════════════
@app.get("/api/units/{unit_id}/vocabulary", response_model=List[VocabularyOut])
async def get_vocabulary(unit_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Vocabulary)
        .where(Vocabulary.unit_id == unit_id)
        .order_by(Vocabulary.id)
    )
    return result.scalars().all()


@app.get("/api/vocabulary/search")
async def search_vocabulary(q: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Vocabulary).where(
            Vocabulary.word_ar.contains(q) | Vocabulary.translation_tr.contains(q)
        ).limit(20)
    )
    return result.scalars().all()


# ═══════════════════════════════════════════
#  الحوارات (Dialogues)
# ═══════════════════════════════════════════
@app.get("/api/lessons/{lesson_id}/dialogues", response_model=List[DialogueOut])
async def get_dialogues(lesson_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Dialogue)
        .where(Dialogue.lesson_id == lesson_id)
        .order_by(Dialogue.dialogue_number)
    )
    dialogues = result.scalars().all()
    # تحميل السطور لكل حوار
    for d in dialogues:
        lines_result = await db.execute(
            select(DialogueLine)
            .where(DialogueLine.dialogue_id == d.id)
            .order_by(DialogueLine.line_order)
        )
        d.lines = lines_result.scalars().all()
    return dialogues


# ═══════════════════════════════════════════
#  التمارين (Exercises)
# ═══════════════════════════════════════════
@app.get("/api/units/{unit_id}/exercises", response_model=List[ExerciseOut])
async def get_exercises(
    unit_id:    int,
    difficulty: Optional[int] = None,
    ex_type:    Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Exercise).where(Exercise.unit_id == unit_id)
    if difficulty:
        query = query.where(Exercise.difficulty == difficulty)
    if ex_type:
        query = query.where(Exercise.exercise_type == ex_type)
    query = query.order_by(Exercise.exercise_number)
    result = await db.execute(query)
    return result.scalars().all()


@app.post("/api/exercises/submit", response_model=AnswerResult)
async def submit_answer(
    data:       AnswerSubmit,
    student_id: int = Depends(get_current_student),
    db:         AsyncSession = Depends(get_db)
):
    # جلب التمرين
    result = await db.execute(select(Exercise).where(Exercise.id == data.exercise_id))
    exercise = result.scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=404, detail="التمرين غير موجود")

    # التحقق من الإجابة — strip Arabic diacritics and whitespace for comparison
    import unicodedata
    def normalize(s: str) -> str:
        # Remove Arabic diacritics (harakat: U+064B–U+065F, tatweel U+0640)
        return ''.join(c for c in s.strip() if not ('ً' <= c <= 'ٟ') and c != 'ـ').strip().lower()

    is_correct = normalize(data.student_answer) == normalize(exercise.correct_answer)
    points_earned = exercise.points if is_correct else 0

    # حفظ الإجابة
    answer = ExerciseAnswer(
        student_id=student_id,
        exercise_id=data.exercise_id,
        student_answer=data.student_answer,
        is_correct=is_correct,
        points_earned=points_earned,
    )
    db.add(answer)
    await db.commit()

    return AnswerResult(
        is_correct=is_correct,
        correct_answer=exercise.correct_answer,
        explanation_ar=exercise.explanation_ar,
        points_earned=points_earned,
    )


# ═══════════════════════════════════════════
#  تقدم الطالب (Progress)
# ═══════════════════════════════════════════
@app.get("/api/me/progress", response_model=List[ProgressOut])
async def get_my_progress(
    student_id: int = Depends(get_current_student),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudentProgress).where(StudentProgress.student_id == student_id)
    )
    return result.scalars().all()


@app.post("/api/me/progress/update")
async def update_progress(
    unit_id:        int,
    lesson_id:      int,
    score:          int = 0,
    time_spent_sec: int = 0,
    status:         str = "in_progress",
    student_id:     int = Depends(get_current_student),
    db:             AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudentProgress).where(
            and_(
                StudentProgress.student_id == student_id,
                StudentProgress.lesson_id  == lesson_id
            )
        )
    )
    progress = result.scalar_one_or_none()

    if progress:
        progress.score          = max(progress.score, score)
        progress.attempts      += 1
        progress.time_spent_sec += time_spent_sec
        progress.status         = status
        if status == "completed":
            progress.completed_at = datetime.utcnow()
    else:
        progress = StudentProgress(
            student_id=student_id,
            unit_id=unit_id,
            lesson_id=lesson_id,
            score=score,
            attempts=1,
            time_spent_sec=time_spent_sec,
            status=status,
            completed_at=datetime.utcnow() if status == "completed" else None,
        )
        db.add(progress)

    await db.commit()
    return {"message": "تم تحديث التقدم"}


# ═══════════════════════════════════════════
#  بطاقات SRS
# ═══════════════════════════════════════════
@app.get("/api/me/srs/due", response_model=List[SRSCardOut])
async def get_due_srs_cards(
    student_id: int = Depends(get_current_student),
    db: AsyncSession = Depends(get_db)
):
    today = date.today().isoformat()
    result = await db.execute(
        select(SRSCard, Vocabulary)
        .join(Vocabulary, SRSCard.vocabulary_id == Vocabulary.id)
        .where(
            and_(SRSCard.student_id == student_id, SRSCard.next_review <= today)
        )
        .limit(20)
    )
    rows = result.all()
    return [
        SRSCardOut(
            vocabulary_id=row.SRSCard.vocabulary_id,
            word_ar=row.Vocabulary.word_ar,
            translation_tr=row.Vocabulary.translation_tr,
            example_ar=row.Vocabulary.example_ar,
            next_review=row.SRSCard.next_review,
            interval_days=row.SRSCard.interval_days,
        )
        for row in rows
    ]


@app.post("/api/me/srs/review")
async def review_srs_card(
    data:       SRSReview,
    student_id: int = Depends(get_current_student),
    db:         AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SRSCard).where(
            and_(
                SRSCard.student_id    == student_id,
                SRSCard.vocabulary_id == data.vocabulary_id
            )
        )
    )
    card = result.scalar_one_or_none()

    if not card:
        card = SRSCard(student_id=student_id, vocabulary_id=data.vocabulary_id)
        db.add(card)

    srs_result = sm2(
        quality=data.quality,
        repetitions=card.repetitions,
        ease_factor=card.ease_factor,
        interval_days=card.interval_days,
    )

    card.interval_days = srs_result.interval_days
    card.ease_factor   = srs_result.ease_factor
    card.repetitions   = srs_result.repetitions
    card.next_review   = srs_result.next_review
    card.last_reviewed = datetime.utcnow()

    await db.commit()
    return {"next_review": srs_result.next_review, "interval_days": srs_result.interval_days}


@app.post("/api/me/srs/add-unit/{unit_id}")
async def add_unit_to_srs(
    unit_id:    int,
    student_id: int = Depends(get_current_student),
    db:         AsyncSession = Depends(get_db)
):
    """إضافة جميع مفردات وحدة إلى بطاقات SRS للطالب"""
    vocab_result = await db.execute(
        select(Vocabulary).where(Vocabulary.unit_id == unit_id)
    )
    vocabs = vocab_result.scalars().all()
    added = 0
    for v in vocabs:
        exists = await db.execute(
            select(SRSCard).where(
                and_(SRSCard.student_id == student_id, SRSCard.vocabulary_id == v.id)
            )
        )
        if not exists.scalar_one_or_none():
            db.add(SRSCard(
                student_id=student_id,
                vocabulary_id=v.id,
                next_review=date.today().isoformat()
            ))
            added += 1
    await db.commit()
    return {"added": added, "message": f"تمت إضافة {added} بطاقة جديدة"}


# ═══════════════════════════════════════════
#  محادثة الذكاء الاصطناعي (AI Chat)
# ═══════════════════════════════════════════
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(
    data:       ChatRequest,
    student_id: int = Depends(get_current_student),
    db:         AsyncSession = Depends(get_db)
):
    unit_context = ""
    if data.unit_id:
        unit_result = await db.execute(select(Unit).where(Unit.id == data.unit_id))
        unit = unit_result.scalar_one_or_none()
        if unit:
            vocab_result = await db.execute(
                select(Vocabulary).where(Vocabulary.unit_id == data.unit_id).limit(30)
            )
            vocabs = vocab_result.scalars().all()
            vocab_list = "، ".join([v.word_ar for v in vocabs])
            unit_context = f"""
الوحدة الحالية: {unit.title_ar} ({unit.title_tr})
المفردات المستهدفة في هذه الوحدة: {vocab_list}
استخدم هذه المفردات في ردودك قدر الإمكان.
"""

    system_prompt = f"""أنت مساعد لتعليم اللغة العربية لطالب تركي يدرس في كلية الإلهيات.

قواعد صارمة:
1. تحدث بالعربية الفصحى فقط في جميع ردودك
2. إذا أخطأ الطالب في الإعراب أو المفردات، صحح الخطأ بلطف
3. استخدم جملاً بسيطة ومفهومة تناسب المستوى الأول
4. إذا كتب الطالب بالتركية، رد عليه بالعربية وأخبره بلطف أن يحاول بالعربية
5. شجع الطالب وكن إيجابياً دائماً
6. في نهاية كل رد، اقترح جملة تدريبية واحدة للطالب

{unit_context}

تذكر: هدفك هو مساعدة الطالب على التواصل بالعربية بشكل طبيعي."""

    from google.genai import types as genai_types

    # Build full contents list: system prompt injected as first user/model turn
    contents = []
    for m in data.messages:
        role = "user" if m.role == "user" else "model"
        contents.append(genai_types.Content(role=role, parts=[genai_types.Part(text=m.content)]))

    response = await _genai_client.aio.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
        config=genai_types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
        ),
    )
    reply = response.text

    # حفظ الجلسة
    session = AISession(
        student_id=student_id,
        unit_id=data.unit_id,
        messages_count=len(data.messages) + 1,
    )
    db.add(session)
    await db.commit()

    return ChatResponse(reply=reply, corrections=[])


# ═══════════════════════════════════════════
#  لوحة تحكم الأستاذ (Teacher Dashboard)
# ═══════════════════════════════════════════
@app.get("/api/teacher/students", response_model=List[StudentSummary])
async def get_all_students(
    student_id: int = Depends(get_current_student),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).order_by(Student.created_at.desc()))
    students = result.scalars().all()

    summaries = []
    for s in students:
        # إجمالي النقاط
        score_result = await db.execute(
            select(func.sum(ExerciseAnswer.points_earned))
            .where(ExerciseAnswer.student_id == s.id)
        )
        total_score = score_result.scalar() or 0

        # عدد الدروس المكتملة
        lessons_result = await db.execute(
            select(func.count(StudentProgress.id))
            .where(
                and_(
                    StudentProgress.student_id == s.id,
                    StudentProgress.status == "completed"
                )
            )
        )
        lessons_done = lessons_result.scalar() or 0

        summaries.append(StudentSummary(
            student_id=s.id,
            name=s.name,
            email=s.email,
            total_score=total_score,
            lessons_done=lessons_done,
            last_active=s.last_login,
        ))

    return summaries


@app.get("/api/teacher/units/stats", response_model=List[UnitStats])
async def get_unit_stats(
    student_id: int = Depends(get_current_student),
    db: AsyncSession = Depends(get_db)
):
    units_result = await db.execute(select(Unit).order_by(Unit.unit_number))
    units = units_result.scalars().all()
    stats = []

    for unit in units:
        # متوسط النقاط
        avg_result = await db.execute(
            select(func.avg(StudentProgress.score))
            .where(StudentProgress.unit_id == unit.id)
        )
        avg_score = avg_result.scalar() or 0.0

        # نسبة الإكمال
        total_students = await db.execute(select(func.count(Student.id)))
        total = total_students.scalar() or 1

        completed_result = await db.execute(
            select(func.count(StudentProgress.id)).where(
                and_(
                    StudentProgress.unit_id == unit.id,
                    StudentProgress.status  == "completed"
                )
            )
        )
        completed = completed_result.scalar() or 0

        stats.append(UnitStats(
            unit_number=unit.unit_number,
            title_ar=unit.title_ar,
            avg_score=round(avg_score, 1),
            completion_pct=round((completed / total) * 100, 1),
        ))

    return stats


# ─────────────────────────────────────────
#  تشغيل التطبيق
# ─────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
