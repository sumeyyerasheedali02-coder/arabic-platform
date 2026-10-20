from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

# ── Auth ──────────────────────────────────
ClassSection = Literal["A", "B", "C", "D"]
AccountRole = Literal["student", "teacher", "admin"]


class StudentNumberSelection(BaseModel):
    student_number: str = Field(min_length=1, max_length=32, pattern=r"^[0-9]+$")

    @field_validator("student_number", mode="before")
    @classmethod
    def normalize_student_number(cls, value):
        if not isinstance(value, str):
            return value
        return value.strip().translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789"))


class ClassSectionSelection(BaseModel):
    class_section: ClassSection

    @field_validator("class_section", mode="before")
    @classmethod
    def normalize_class_section(cls, value):
        return value.strip().upper() if isinstance(value, str) else value


class StudentProfileCompletion(StudentNumberSelection):
    class_section: Optional[ClassSection] = None

    @field_validator("class_section", mode="before")
    @classmethod
    def normalize_class_section(cls, value):
        return ClassSectionSelection.normalize_class_section(value)


class StudentRegister(ClassSectionSelection, StudentNumberSelection):
    name:     str
    email:    EmailStr
    password: str = Field(min_length=6)

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, value: str) -> str:
        # bcrypt only looks at the first 72 bytes (and newer versions refuse more).
        # Arabic letters take two bytes each.
        if len(value.encode("utf-8")) > 72:
            raise ValueError("كلمة المرور طويلة جداً")
        return value

class StudentLogin(BaseModel):
    email:    EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    student_id:   int
    name:         str
    is_teacher:   bool = False
    class_section: Optional[ClassSection] = None
    role: AccountRole = "student"
    is_admin: bool = False
    student_number: Optional[str] = None

class EmailCheckResponse(BaseModel):
    exists: bool
    name:   Optional[str] = None

class SessionInfo(BaseModel):
    student_id: int
    name:       str
    is_teacher: bool
    class_section: Optional[ClassSection] = None
    role: AccountRole = "student"
    is_admin: bool = False
    student_number: Optional[str] = None


class TeacherCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=10)
    sections: List[ClassSection] = Field(min_length=1, max_length=4)

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, value):
        return StudentRegister.password_fits_bcrypt(value)

    @field_validator("name")
    @classmethod
    def nonempty_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("الاسم مطلوب")
        return value


class TeacherUpdate(BaseModel):
    sections: List[ClassSection] = Field(max_length=4)
    is_active: bool
    password: Optional[str] = Field(default=None, min_length=10)

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, value):
        return StudentRegister.password_fits_bcrypt(value) if value is not None else value


class TeacherInfo(BaseModel):
    id: int
    name: str
    email: str
    sections: List[ClassSection]
    is_active: bool


class SectionInfo(BaseModel):
    class_section: ClassSection
    students_count: int
    teachers_count: int


# ── Vocabulary ────────────────────────────
class VocabularyOut(BaseModel):
    id:             int
    lesson_id:      Optional[int]
    word_ar:        str
    word_type:      Optional[str]
    gender:         Optional[str]
    plural_ar:      Optional[str]
    translation_tr: str
    translation_en: Optional[str]
    example_ar:     Optional[str]
    example_tr:     Optional[str]
    difficulty:     int

    model_config = {"from_attributes": True}


# ── Dialogue ──────────────────────────────
class DialogueLineOut(BaseModel):
    line_order:     int
    speaker:        str
    text_ar:        str
    translation_tr: Optional[str]
    is_key_phrase:  bool

    model_config = {"from_attributes": True}

class DialogueOut(BaseModel):
    id:              int
    dialogue_number: int
    title_ar:        Optional[str]
    situation_tr:    Optional[str]
    lines:           List[DialogueLineOut]
    audio_url:       Optional[str] = None
    audio_is_partial: bool = False
    audio_text_differs: bool = False

    model_config = {"from_attributes": True}


# ── Exercise ──────────────────────────────
class ExerciseOut(BaseModel):
    id:              int
    unit_id:         int
    lesson_id:       Optional[int]
    exercise_number: int
    exercise_type:   str
    # synonym | antonym | plural | comprehension | word_order | null
    category:        Optional[str] = None
    question_ar:     str
    correct_answer:  Optional[str] = None
    question_tr:     Optional[str]
    options:         Optional[Any]
    hint_ar:         Optional[str]
    hint_tr:         Optional[str]
    difficulty:      int
    points:          int

    model_config = {"from_attributes": True}

class AnswerSubmit(BaseModel):
    exercise_id:    int
    student_answer: str

class AnswerResult(BaseModel):
    is_correct:     bool
    correct_answer: str
    explanation_ar: Optional[str]
    points_earned:  int


# ── Lesson ────────────────────────────────
class LessonOut(BaseModel):
    id:            int
    unit_id:       Optional[int] = None
    lesson_number: int
    title_ar:      str
    title_tr:      Optional[str]
    lesson_type:   Optional[str]
    grammar_focus: Optional[str]
    content_ar:    Optional[str] = None

    model_config = {"from_attributes": True}


# ── Unit ──────────────────────────────────
class UnitOut(BaseModel):
    id:             int
    unit_number:    int
    title_ar:       str
    title_tr:       str
    description_ar: Optional[str]
    description_tr: Optional[str]
    total_lessons:  int

    model_config = {"from_attributes": True}


# ── Progress ──────────────────────────────
class ProgressOut(BaseModel):
    unit_id:        int
    lesson_id:      int
    status:         str
    score:          int
    attempts:       int
    time_spent_sec: int

    model_config = {"from_attributes": True}


# ── AI Chat ───────────────────────────────
class ChatMessage(BaseModel):
    role:    str   # "user"; anything else ("model", "assistant") is the tutor
    content: str = Field(min_length=1, max_length=4000)

class ChatRequest(BaseModel):
    unit_id:  Optional[int] = None
    # The whole conversation so far, oldest first; the last entry is the new message.
    messages: List[ChatMessage] = Field(min_length=1)

class ChatResponse(BaseModel):
    reply:       str
    corrections: List[str] = []


# ── SRS ───────────────────────────────────
class SRSReview(BaseModel):
    vocabulary_id: int
    quality: int = Field(ge=0, le=5)  # 0=فشل تام، 5=ممتاز

class SRSCardOut(BaseModel):
    vocabulary_id:  int
    word_ar:        str
    translation_tr: str
    example_ar:     Optional[str]
    next_review:    Optional[str]
    interval_days:  int
    # rating (0–5) -> days until the next review if the card gets that rating
    next_interval_days: Dict[int, int] = {}

    model_config = {"from_attributes": True}


# ── Dashboard (للأستاذ) ───────────────────
class StudentSummary(BaseModel):
    active_time_sec: int = 0
    student_id:      int
    name:            str
    email:           str
    student_number:  Optional[str] = None
    class_section:   Optional[ClassSection] = None
    total_score:     int
    lessons_done:    int
    last_active:     Optional[datetime]
    completion_pct: float = 0
    answers_count: int = 0
    correct_answers: int = 0
    accuracy_pct: Optional[float] = None

class UnitStats(BaseModel):
    unit_number:    int
    title_ar:       str
    avg_score:      float
    completion_pct: float
