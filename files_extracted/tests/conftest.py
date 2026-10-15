import itertools
from types import SimpleNamespace

import httpx
import pytest
import pytest_asyncio
from sqlalchemy import event

from . import _app
from ._app import AsyncSessionLocal, Base, engine, hash_password, models

_counter = itertools.count(1)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _schema():
    database = str(engine.url.database or "")
    on_throwaway_database = "arabiq-test-" in database or _app.TEST_DATABASE_MARKER in database
    assert on_throwaway_database, "tests must run on a throw-away database"
    await _app.init_db()
    yield
    await engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def content(_schema):
    """Empty every table, then load a small deterministic content set."""
    async with AsyncSessionLocal() as db:
        for table in reversed(Base.metadata.sorted_tables):
            await db.execute(table.delete())
        await db.commit()

        # Inserted out of order on purpose: the API must sort by unit_number.
        unit_b = models.Unit(unit_number=2, title_ar="الأُسْرَة", title_tr="Aile", total_lessons=3)
        unit_a = models.Unit(unit_number=1, title_ar="التَّحِيَّة", title_tr="Selamlama", total_lessons=3)
        db.add_all([unit_b, unit_a])
        await db.flush()

        def lessons_for(unit, grammar):
            return [
                models.Lesson(unit_id=unit.id, lesson_number=1, title_ar="الحِوَارَات",
                              title_tr="Diyaloglar", lesson_type="hiwar"),
                models.Lesson(unit_id=unit.id, lesson_number=2, title_ar="المُفْرَدَات",
                              title_tr="Kelimeler", lesson_type="mufradat"),
                models.Lesson(unit_id=unit.id, lesson_number=3, title_ar="النَّحْو",
                              title_tr="Dilbilgisi", lesson_type="nahw", grammar_focus=grammar),
            ]

        a_hiwar, a_muf, a_nahw = lessons_for(unit_a, "قاعدة أولى | قاعدة ثانية")
        b_hiwar, b_muf, b_nahw = lessons_for(unit_b, "قاعدة")
        db.add_all([a_hiwar, a_muf, a_nahw, b_hiwar, b_muf, b_nahw])
        await db.flush()

        words_a = [("كِتَاب", "kitap", "book"), ("قَلَم", "kalem", "pen"),
                   ("بَيْت", "ev", "house"), ("مَدْرَسَة", "okul", "school")]
        vocab_a = [models.Vocabulary(unit_id=unit_a.id, lesson_id=a_muf.id, word_ar=ar,
                                     translation_tr=tr, translation_en=en, example_ar=f"هذا {ar}")
                   for ar, tr, en in words_a]
        vocab_b = [models.Vocabulary(unit_id=unit_b.id, lesson_id=b_muf.id, word_ar=ar,
                                     translation_tr=tr, translation_en=en)
                   for ar, tr, en in [("أَب", "baba", "father"), ("أُمّ", "anne", "mother")]]
        db.add_all(vocab_a + vocab_b)

        dialogue = models.Dialogue(lesson_id=a_hiwar.id, dialogue_number=1,
                                   title_ar="الحوار الأول", situation_tr="Halid, Halil")
        db.add(dialogue)
        await db.flush()
        # Lines inserted out of order on purpose.
        db.add_all([
            models.DialogueLine(dialogue_id=dialogue.id, line_order=2, speaker="خليل",
                                text_ar="وَعَلَيْكُمُ السَّلَام."),
            models.DialogueLine(dialogue_id=dialogue.id, line_order=1, speaker="خالد",
                                text_ar="السَّلَامُ عَلَيْكُم."),
        ])

        ex_choice = models.Exercise(
            unit_id=unit_a.id, lesson_id=a_muf.id, exercise_number=1,
            exercise_type="multiple_choice", question_ar="مَا مَعْنَى كَلِمَة: كِتَاب؟",
            correct_answer="kitap", options=["kalem", "kitap", "ev", "okul"],
            difficulty=1, points=10)
        ex_true_false = models.Exercise(
            unit_id=unit_a.id, lesson_id=a_muf.id, exercise_number=2,
            exercise_type="true_false", question_ar="هَلْ مَعْنَى «قَلَم»: «kalem»؟",
            correct_answer="صَحِيح", options=["صَحِيح", "خَطَأ"], difficulty=1, points=5)
        ex_blank = models.Exercise(
            unit_id=unit_a.id, lesson_id=a_hiwar.id, exercise_number=3,
            exercise_type="fill_blank", question_ar="السلام ___________.",
            correct_answer="عَلَيْكُم", hint_ar="تحية", explanation_ar="رد التحية",
            difficulty=2, points=10)
        ex_synonym = models.Exercise(
            unit_id=unit_a.id, lesson_id=a_nahw.id, exercise_number=4,
            exercise_type="multiple_choice", question_ar="مدرّس — ما الكلمة المرادفة؟",
            correct_answer="أستاذ", options=["أستاذ", "طالب", "طبيب", "مهندس"],
            hint_ar="مترادف", difficulty=3, points=15)
        ex_order = models.Exercise(
            unit_id=unit_a.id, lesson_id=a_hiwar.id, exercise_number=5,
            exercise_type="fill_blank", question_ar="رَتِّب الكلمات: خالد / اسمي",
            correct_answer="اسمي خالد", difficulty=3, points=15)
        ex_unit_b = models.Exercise(
            unit_id=unit_b.id, lesson_id=b_muf.id, exercise_number=1,
            exercise_type="multiple_choice", question_ar="مَا مَعْنَى كَلِمَة: أَب؟",
            correct_answer="baba", options=["baba", "anne"], difficulty=1, points=10)
        db.add_all([ex_choice, ex_true_false, ex_blank, ex_synonym, ex_order, ex_unit_b])
        await db.commit()

        return SimpleNamespace(
            unit_a=unit_a.id, unit_b=unit_b.id,
            a_hiwar=a_hiwar.id, a_muf=a_muf.id, a_nahw=a_nahw.id,
            b_hiwar=b_hiwar.id, b_muf=b_muf.id, b_nahw=b_nahw.id,
            vocab_a=[v.id for v in vocab_a], vocab_b=[v.id for v in vocab_b],
            dialogue=dialogue.id,
            ex_choice=ex_choice.id, ex_true_false=ex_true_false.id, ex_blank=ex_blank.id,
            ex_synonym=ex_synonym.id, ex_order=ex_order.id, ex_unit_b=ex_unit_b.id,
        )


@pytest_asyncio.fixture
async def client():
    transport = httpx.ASGITransport(app=_app.app, raise_app_exceptions=False)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def db():
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture
def new_email():
    def _make(prefix="student"):
        return f"{prefix}{next(_counter)}@example.com"
    return _make


@pytest.fixture
def register(client, new_email):
    """Register a student through the API; returns auth headers plus identity."""
    async def _register(email=None, name="Ayşe Yılmaz", password="secret123", class_section="A",
                        student_number=None):
        email = email or new_email()
        student_number = student_number if student_number is not None else f"00{next(_counter):08d}"
        res = await client.post("/api/auth/register", json={
            "name": name, "email": email, "password": password, "class_section": class_section,
            "student_number": student_number})
        assert res.status_code == 200, res.text
        body = res.json()
        return SimpleNamespace(
            headers={"Authorization": f"Bearer {body['access_token']}"},
            id=body["student_id"], email=email, password=password, body=body,
            student_number=body["student_number"])
    return _register


@pytest.fixture
def login(client):
    async def _login(email, password):
        return await client.post("/api/auth/login", data={"username": email, "password": password})
    return _login


@pytest.fixture
def teacher(login):
    """Provision the teacher account directly (not through public registration)."""
    async def _teacher(password="teacher-pass-1", sections=("A", "B", "C", "D"), email=None):
        async with AsyncSessionLocal() as session:
            account = models.Student(name="Öğretmen", email=email or _app.TEACHER_EMAIL,
                                     password_hash=hash_password(password), role="teacher")
            session.add(account)
            await session.flush()
            session.add_all([models.TeacherSection(teacher_id=account.id, class_section=s)
                             for s in sections])
            await session.commit()
            account_id = account.id
        res = await login(email or _app.TEACHER_EMAIL, password)
        assert res.status_code == 200, res.text
        body = res.json()
        return SimpleNamespace(
            headers={"Authorization": f"Bearer {body['access_token']}"}, id=account_id, body=body)
    return _teacher


@pytest.fixture
def admin(login):
    async def _admin():
        async with AsyncSessionLocal() as session:
            account = models.Student(name="Malek", email="malekco721@gmail.com",
                                     password_hash=hash_password("admin-test-pass"), role="admin")
            session.add(account)
            await session.commit()
        res = await login(account.email, "admin-test-pass")
        assert res.status_code == 200, res.text
        body = res.json()
        return SimpleNamespace(id=account.id, headers={"Authorization": f"Bearer {body['access_token']}"},
                               body=body)
    return _admin


class FakeAI:
    """Stands in for the Gemini client so no test ever calls the real provider."""

    def __init__(self):
        self.calls = []
        self.reply = "أَحْسَنْتَ! جملة التدريب: اسمي خالد."
        self.error = None
        self.aio = SimpleNamespace(models=SimpleNamespace(
            generate_content=self._generate, generate_content_stream=self._stream))

    async def _generate(self, *, model, contents, config):
        self.calls.append(SimpleNamespace(model=model, contents=contents, config=config))
        if self.error:
            raise self.error
        return SimpleNamespace(text=self.reply)

    async def _stream(self, **kwargs):
        await self._generate(**kwargs)

        async def chunks():
            if self.reply:
                yield SimpleNamespace(text=self.reply[:4])
                yield SimpleNamespace(text=self.reply[4:])
        return chunks()


@pytest.fixture
def fake_ai(monkeypatch):
    fake = FakeAI()
    monkeypatch.setattr(_app.ai_service, "get_client", lambda: fake)
    return fake


@pytest.fixture
def seed_spy(monkeypatch):
    """Replace the content seeder with a recorder: the real one wipes student activity."""
    from tools import seed as seed_tool

    calls = []

    async def _fake_seed(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr(seed_tool, "seed", _fake_seed)
    return calls


@pytest.fixture
def count_queries():
    """Context manager counting SQL statements sent to the database."""
    class _Counter:
        def __enter__(self):
            self.statements = []
            event.listen(engine.sync_engine, "before_cursor_execute", self._on_execute)
            return self

        def __exit__(self, *exc):
            event.remove(engine.sync_engine, "before_cursor_execute", self._on_execute)

        def _on_execute(self, conn, cursor, statement, parameters, context, executemany):
            self.statements.append(statement)

        @property
        def count(self):
            return len(self.statements)

    return _Counter
