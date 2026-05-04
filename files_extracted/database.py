from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./arabic_platform.db")

# Railway provides postgres:// or postgresql:// — asyncpg requires the +asyncpg driver prefix
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# ─────────────────────────────────────────
#  الوحدات
# ─────────────────────────────────────────
class Unit(Base):
    __tablename__ = "units"
    id             = Column(Integer, primary_key=True, index=True)
    unit_number    = Column(Integer, unique=True, nullable=False)
    title_ar       = Column(Text, nullable=False)
    title_tr       = Column(Text, nullable=False)
    description_ar = Column(Text)
    description_tr = Column(Text)
    total_lessons  = Column(Integer, default=0)

    lessons        = relationship("Lesson",    back_populates="unit", cascade="all, delete")
    vocabulary     = relationship("Vocabulary", back_populates="unit", cascade="all, delete")
    exercises      = relationship("Exercise",  back_populates="unit", cascade="all, delete")


# ─────────────────────────────────────────
#  الدروس
# ─────────────────────────────────────────
class Lesson(Base):
    __tablename__ = "lessons"
    id             = Column(Integer, primary_key=True, index=True)
    unit_id        = Column(Integer, ForeignKey("units.id", ondelete="CASCADE"))
    lesson_number  = Column(Integer, nullable=False)
    title_ar       = Column(Text, nullable=False)
    title_tr       = Column(Text)
    lesson_type    = Column(String(20))
    content_ar     = Column(Text)
    grammar_focus  = Column(Text)
    page_number    = Column(Integer)

    unit           = relationship("Unit",      back_populates="lessons")
    vocabulary     = relationship("Vocabulary", back_populates="lesson")
    exercises      = relationship("Exercise",  back_populates="lesson", cascade="all, delete")
    dialogues      = relationship("Dialogue",  back_populates="lesson", cascade="all, delete")


# ─────────────────────────────────────────
#  المفردات
# ─────────────────────────────────────────
class Vocabulary(Base):
    __tablename__ = "vocabulary"
    id             = Column(Integer, primary_key=True, index=True)
    unit_id        = Column(Integer, ForeignKey("units.id",   ondelete="CASCADE"))
    lesson_id      = Column(Integer, ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True)
    word_ar        = Column(Text, nullable=False)
    word_root      = Column(Text)
    word_type      = Column(String(20))
    gender         = Column(String(10))
    plural_ar      = Column(Text)
    translation_tr = Column(Text, nullable=False)
    translation_en = Column(Text)
    example_ar     = Column(Text)
    example_tr     = Column(Text)
    audio_url      = Column(Text)
    difficulty     = Column(Integer, default=1)

    unit           = relationship("Unit",   back_populates="vocabulary")
    lesson         = relationship("Lesson", back_populates="vocabulary")
    srs_cards      = relationship("SRSCard", back_populates="vocabulary", cascade="all, delete")


# ─────────────────────────────────────────
#  الحوارات
# ─────────────────────────────────────────
class Dialogue(Base):
    __tablename__ = "dialogues"
    id               = Column(Integer, primary_key=True, index=True)
    lesson_id        = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"))
    dialogue_number  = Column(Integer, nullable=False)
    title_ar         = Column(Text)
    situation_tr     = Column(Text)

    lesson           = relationship("Lesson", back_populates="dialogues")
    lines            = relationship("DialogueLine", back_populates="dialogue", cascade="all, delete", order_by="DialogueLine.line_order")


class DialogueLine(Base):
    __tablename__ = "dialogue_lines"
    id             = Column(Integer, primary_key=True, index=True)
    dialogue_id    = Column(Integer, ForeignKey("dialogues.id", ondelete="CASCADE"))
    line_order     = Column(Integer, nullable=False)
    speaker        = Column(Text, nullable=False)
    text_ar        = Column(Text, nullable=False)
    translation_tr = Column(Text)
    is_key_phrase  = Column(Boolean, default=False)

    dialogue       = relationship("Dialogue", back_populates="lines")


# ─────────────────────────────────────────
#  التمارين
# ─────────────────────────────────────────
class Exercise(Base):
    __tablename__ = "exercises"
    id               = Column(Integer, primary_key=True, index=True)
    lesson_id        = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True)
    unit_id          = Column(Integer, ForeignKey("units.id",   ondelete="CASCADE"))
    exercise_number  = Column(Integer, nullable=False)
    exercise_type    = Column(String(30), nullable=False)
    question_ar      = Column(Text, nullable=False)
    question_tr      = Column(Text)
    correct_answer   = Column(Text, nullable=False)
    options          = Column(JSON)
    hint_ar          = Column(Text)
    hint_tr          = Column(Text)
    explanation_ar   = Column(Text)
    difficulty       = Column(Integer, default=1)
    points           = Column(Integer, default=10)

    unit             = relationship("Unit",   back_populates="exercises")
    lesson           = relationship("Lesson", back_populates="exercises")
    answers          = relationship("ExerciseAnswer", back_populates="exercise", cascade="all, delete")


# ─────────────────────────────────────────
#  الطلاب
# ─────────────────────────────────────────
class Student(Base):
    __tablename__ = "students"
    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(Text, nullable=False)
    email          = Column(Text, unique=True, nullable=False, index=True)
    password_hash  = Column(Text, nullable=False)
    university     = Column(Text, default="Karabük Üniversitesi")
    department     = Column(Text, default="İlahiyat Fakültesi")
    year           = Column(Integer, default=1)
    language_pref  = Column(String(5), default="tr")
    created_at     = Column(DateTime, server_default=func.now())
    last_login     = Column(DateTime)

    progress       = relationship("StudentProgress", back_populates="student", cascade="all, delete")
    answers        = relationship("ExerciseAnswer",  back_populates="student", cascade="all, delete")
    srs_cards      = relationship("SRSCard",         back_populates="student", cascade="all, delete")
    ai_sessions    = relationship("AISession",       back_populates="student", cascade="all, delete")


# ─────────────────────────────────────────
#  تقدم الطلاب
# ─────────────────────────────────────────
class StudentProgress(Base):
    __tablename__ = "student_progress"
    id              = Column(Integer, primary_key=True, index=True)
    student_id      = Column(Integer, ForeignKey("students.id",  ondelete="CASCADE"))
    unit_id         = Column(Integer, ForeignKey("units.id"))
    lesson_id       = Column(Integer, ForeignKey("lessons.id"))
    status          = Column(String(20), default="not_started")
    score           = Column(Integer, default=0)
    attempts        = Column(Integer, default=0)
    time_spent_sec  = Column(Integer, default=0)
    completed_at    = Column(DateTime)
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now())

    student         = relationship("Student", back_populates="progress")


# ─────────────────────────────────────────
#  إجابات التمارين
# ─────────────────────────────────────────
class ExerciseAnswer(Base):
    __tablename__ = "exercise_answers"
    id              = Column(Integer, primary_key=True, index=True)
    student_id      = Column(Integer, ForeignKey("students.id",   ondelete="CASCADE"))
    exercise_id     = Column(Integer, ForeignKey("exercises.id",  ondelete="CASCADE"))
    student_answer  = Column(Text, nullable=False)
    is_correct      = Column(Boolean, nullable=False)
    points_earned   = Column(Integer, default=0)
    answered_at     = Column(DateTime, server_default=func.now())

    student         = relationship("Student",  back_populates="answers")
    exercise        = relationship("Exercise", back_populates="answers")


# ─────────────────────────────────────────
#  بطاقات SRS
# ─────────────────────────────────────────
class SRSCard(Base):
    __tablename__ = "srs_cards"
    id              = Column(Integer, primary_key=True, index=True)
    student_id      = Column(Integer, ForeignKey("students.id",    ondelete="CASCADE"))
    vocabulary_id   = Column(Integer, ForeignKey("vocabulary.id",  ondelete="CASCADE"))
    ease_factor     = Column(Float, default=2.5)
    interval_days   = Column(Integer, default=1)
    repetitions     = Column(Integer, default=0)
    next_review     = Column(Text)        # ISO date string
    last_reviewed   = Column(DateTime)

    student         = relationship("Student",    back_populates="srs_cards")
    vocabulary      = relationship("Vocabulary", back_populates="srs_cards")


# ─────────────────────────────────────────
#  جلسات الذكاء الاصطناعي
# ─────────────────────────────────────────
class AISession(Base):
    __tablename__ = "ai_sessions"
    id              = Column(Integer, primary_key=True, index=True)
    student_id      = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    unit_id         = Column(Integer, ForeignKey("units.id"), nullable=True)
    session_start   = Column(DateTime, server_default=func.now())
    session_end     = Column(DateTime)
    messages_count  = Column(Integer, default=0)
    corrections     = Column(JSON, default=list)

    student         = relationship("Student", back_populates="ai_sessions")


# ─────────────────────────────────────────
#  Dependency
# ─────────────────────────────────────────
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
