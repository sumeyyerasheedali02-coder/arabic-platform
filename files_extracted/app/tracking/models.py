"""New names deliberately avoid Railway's existing, undocumented grade_* tables."""
from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)

from app.database import Base


class TrackingCycle(Base):
    __tablename__ = "takip_cycles"
    __table_args__ = (
        UniqueConstraint("academic_year", "section"),
        CheckConstraint("section IN ('A', 'B', 'C', 'D')"),
    )
    id = Column(Integer, primary_key=True)
    academic_year = Column(String(9), nullable=False)
    section = Column(String(1), nullable=False)
    revision = Column(Integer, nullable=False, default=0)
    final_published = Column(Boolean, nullable=False, default=False)


class TrackingWeek(Base):
    __tablename__ = "takip_weeks"
    __table_args__ = (UniqueConstraint("cycle_id", "number"), CheckConstraint("number BETWEEN 1 AND 52"))
    id = Column(Integer, primary_key=True)
    cycle_id = Column(Integer, ForeignKey("takip_cycles.id"), nullable=False)
    number = Column(Integer, nullable=False)
    starts_on = Column(Date, nullable=False)
    published = Column(Boolean, nullable=False, default=False)


class TrackingEntry(Base):
    __tablename__ = "takip_entries"
    __table_args__ = (
        UniqueConstraint("week_id", "student_id"),
        *(CheckConstraint(f"{key} BETWEEN 0 AND 10") for key in
          ("writing", "class_activity", "home_activity", "language_lab")),
    )
    id = Column(Integer, primary_key=True)
    week_id = Column(Integer, ForeignKey("takip_weeks.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    writing = Column(Float)
    class_activity = Column(Float)
    home_activity = Column(Float)
    language_lab = Column(Float)
    note = Column(Text, nullable=False, default="")


class TrackingTerm(Base):
    __tablename__ = "takip_terms"
    __table_args__ = (
        UniqueConstraint("cycle_id", "number"),
        CheckConstraint("number IN (1, 2)"),
        CheckConstraint("first_week >= 1 AND last_week <= 52 AND last_week >= first_week"),
    )
    id = Column(Integer, primary_key=True)
    cycle_id = Column(Integer, ForeignKey("takip_cycles.id"), nullable=False)
    number = Column(Integer, nullable=False)
    first_week = Column(Integer, nullable=False)
    last_week = Column(Integer, nullable=False)
    published = Column(Boolean, nullable=False, default=False)


class TrackingExam(Base):
    __tablename__ = "takip_exams"
    __table_args__ = (UniqueConstraint("term_id", "student_id"), CheckConstraint("score BETWEEN 0 AND 60"))
    id = Column(Integer, primary_key=True)
    term_id = Column(Integer, ForeignKey("takip_terms.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    score = Column(Float)


class TrackingAudit(Base):
    __tablename__ = "takip_audit"
    id = Column(Integer, primary_key=True)
    cycle_id = Column(Integer, ForeignKey("takip_cycles.id"), nullable=False, index=True)
    actor_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    action = Column(String(40), nullable=False)
    details = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
