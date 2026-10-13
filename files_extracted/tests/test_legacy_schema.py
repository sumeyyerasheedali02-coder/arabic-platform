"""The actual Railway legacy layout must retain data and accept the new ORM."""
import uuid

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.legacy_schema import align_legacy_sections
from app.migrations import apply_migrations
from app.models import Student, TeacherSection

from ._app import Base, engine


@pytest.mark.skipif(engine.dialect.name != "postgresql", reason="Railway legacy layout is PostgreSQL")
async def test_railway_sections_keep_values_and_accept_both_column_names():
    schema = "legacy_test_" + uuid.uuid4().hex
    async with engine.begin() as conn:
        await conn.execute(text(f"CREATE SCHEMA {schema}"))
        await conn.execute(text(f"SET LOCAL search_path TO {schema}"))
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("ALTER TABLE students RENAME COLUMN class_section TO section"))
        await conn.execute(text(
            "ALTER TABLE students RENAME CONSTRAINT ck_students_class_section TO ck_students_section"))
        for column in ("is_active", "token_version", "student_number"):
            await conn.execute(text(f"ALTER TABLE students DROP COLUMN {column}"))
        await conn.execute(text("DROP TABLE teacher_sections"))
        await conn.execute(text("""
            CREATE TABLE teacher_sections (
                id SERIAL PRIMARY KEY,
                teacher_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                section VARCHAR(1) NOT NULL CHECK (section IN ('A','B','C','D')),
                created_at TIMESTAMP DEFAULT now(), UNIQUE (teacher_id, section)
            )
        """))
        await conn.execute(text("""
            INSERT INTO students (id,name,email,password_hash,role,section) VALUES
            (100,'Owner','malekco721@gmail.com','owner-original-hash','admin',NULL),
            (101,'Teacher','legacy-teacher@example.com','teacher-original-hash','teacher',NULL),
            (102,'Other admin','other-admin@example.com','admin-original-hash','admin',NULL),
            (103,'Student','student@example.com','student-original-hash','student','A')
        """))
        await conn.execute(text("INSERT INTO teacher_sections (teacher_id,section) VALUES (101,'A')"))
        before = (await conn.execute(text(
            "SELECT id,name,email,password_hash,role,section FROM students ORDER BY id"))).all()
        link_before = (await conn.execute(text(
            "SELECT id,teacher_id,section,created_at FROM teacher_sections"))).all()

        await align_legacy_sections(conn)
        assert len(await apply_migrations(conn)) == 5
        assert (await conn.execute(text(
            "SELECT id,name,email,password_hash,role,section FROM students ORDER BY id"))).all() == before
        assert (await conn.execute(text(
            "SELECT id,teacher_id,section,created_at FROM teacher_sections"))).all() == link_before
        assert (await conn.execute(text(
            "SELECT class_section FROM students WHERE id=103"))).scalar_one() == "A"
        assert (await conn.execute(text(
            "SELECT COUNT(*) FROM students WHERE student_number IS NOT NULL"))).scalar_one() == 0

        async with AsyncSession(bind=conn, expire_on_commit=False) as db:
            # New code omits legacy id/section/created_at on a teacher assignment.
            db.add(TeacherSection(teacher_id=101, class_section="B"))
            await db.flush()
            assert (await conn.execute(text(
                "SELECT section FROM teacher_sections WHERE teacher_id=101 AND class_section='B'"
            ))).scalar_one() == "B"
            student = (await db.execute(select(Student).where(Student.id == 103))).scalar_one()
            student.class_section = "C"
            await db.flush()
            assert (await conn.execute(text(
                "SELECT section FROM students WHERE id=103"))).scalar_one() == "C"
            new_student = Student(name="New", email="new@example.com", password_hash="new-hash",
                                  class_section="D", student_number="00123")
            db.add(new_student)
            await db.flush()
            assert (await conn.execute(text(
                "SELECT section FROM students WHERE id=:id"), {"id": new_student.id}
            )).scalar_one() == "D"

        # An older writer can still use the old field without erasing the new one.
        await conn.execute(text("UPDATE students SET section='B' WHERE id=103"))
        assert (await conn.execute(text(
            "SELECT class_section FROM students WHERE id=103"))).scalar_one() == "B"
        await align_legacy_sections(conn)
        assert await apply_migrations(conn) == []
        await conn.execute(text("SET LOCAL search_path TO public"))
        await conn.execute(text(f"DROP SCHEMA {schema} CASCADE"))
