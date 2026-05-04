from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from datetime import datetime


# ── Auth ──────────────────────────────────
class StudentRegister(BaseModel):
    name:     str
    email:    EmailStr
    password: str = Field(min_length=6)
    year:     Optional[int] = 1

class StudentLogin(BaseModel):
    email:    EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    student_id:   int
    name:         str

class EmailCheckResponse(BaseModel):
    exists: bool
    name:   Optional[str] = None


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

    model_config = {"from_attributes": True}


# ── Exercise ──────────────────────────────
class ExerciseOut(BaseModel):
    id:              int
    unit_id:         int
    lesson_id:       Optional[int]
    exercise_number: int
    exercise_type:   str
    question_ar:     str
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
    lesson_number: int
    title_ar:      str
    title_tr:      Optional[str]
    lesson_type:   Optional[str]
    grammar_focus: Optional[str]

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
    role:    str   # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    unit_id:  Optional[int] = None
    messages: List[ChatMessage]

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

    model_config = {"from_attributes": True}


# ── Dashboard (للأستاذ) ───────────────────
class StudentSummary(BaseModel):
    student_id:      int
    name:            str
    email:           str
    total_score:     int
    lessons_done:    int
    last_active:     Optional[datetime]

class UnitStats(BaseModel):
    unit_number:    int
    title_ar:       str
    avg_score:      float
    completion_pct: float
