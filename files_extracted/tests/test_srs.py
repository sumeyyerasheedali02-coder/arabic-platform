from datetime import date, timedelta

from sqlalchemy import select

from app.services.srs import preview_intervals, sm2

from ._app import models


def _iso(days):
    return (date.today() + timedelta(days=days)).isoformat()


# ── SM-2 (pure) ───────────────────────────────────────────────

def test_sm2_first_two_successes_use_fixed_intervals():
    first = sm2(quality=5, repetitions=0, ease_factor=2.5, interval_days=1)
    assert (first.interval_days, first.repetitions, first.next_review) == (1, 1, _iso(1))
    second = sm2(quality=5, repetitions=1, ease_factor=first.ease_factor, interval_days=1)
    assert (second.interval_days, second.repetitions) == (6, 2)


def test_sm2_later_successes_multiply_by_ease_factor():
    result = sm2(quality=4, repetitions=2, ease_factor=2.5, interval_days=6)
    assert result.interval_days == 15 and result.ease_factor == 2.5


def test_sm2_failure_resets_and_ease_factor_has_a_floor():
    result = sm2(quality=1, repetitions=5, ease_factor=1.3, interval_days=40)
    assert (result.interval_days, result.repetitions, result.ease_factor) == (1, 0, 1.3)


# ── API ───────────────────────────────────────────────────────

async def test_srs_requires_login(client, content):
    assert (await client.get("/api/me/srs/due")).status_code == 401
    assert (await client.post(f"/api/me/srs/add-unit/{content.unit_a}")).status_code == 401
    res = await client.post("/api/me/srs/review", json={"vocabulary_id": content.vocab_a[0], "quality": 5})
    assert res.status_code == 401


async def test_adding_a_unit_creates_one_due_card_per_word_once(client, register, content):
    student = await register()
    first = await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)
    again = await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)
    assert first.json()["added"] == 4 and again.json()["added"] == 0

    due = (await client.get("/api/me/srs/due", headers=student.headers)).json()
    assert sorted(card["vocabulary_id"] for card in due) == sorted(content.vocab_a)
    card = next(c for c in due if c["vocabulary_id"] == content.vocab_a[0])
    assert (card["word_ar"], card["translation_tr"], card["example_ar"]) == ("كِتَاب", "kitap", "هذا كِتَاب")


async def test_due_cards_belong_to_the_caller_only(client, register, content):
    owner, other = await register(), await register()
    await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=owner.headers)
    assert (await client.get("/api/me/srs/due", headers=other.headers)).json() == []


async def test_review_schedules_the_card_and_removes_it_from_due(client, register, content):
    student = await register()
    await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)
    word = content.vocab_a[0]

    first = await client.post("/api/me/srs/review", headers=student.headers,
                              json={"vocabulary_id": word, "quality": 5})
    assert first.json() == {"next_review": _iso(1), "interval_days": 1}
    second = await client.post("/api/me/srs/review", headers=student.headers,
                               json={"vocabulary_id": word, "quality": 5})
    assert second.json() == {"next_review": _iso(6), "interval_days": 6}

    due = (await client.get("/api/me/srs/due", headers=student.headers)).json()
    assert word not in [card["vocabulary_id"] for card in due]


async def test_review_rejects_out_of_range_quality(client, register, content):
    student = await register()
    res = await client.post("/api/me/srs/review", headers=student.headers,
                            json={"vocabulary_id": content.vocab_a[0], "quality": 6})
    assert res.status_code == 422


async def test_reviewing_a_word_without_a_card_creates_the_card(client, register, content, db):
    student = await register()
    res = await client.post("/api/me/srs/review", headers=student.headers,
                            json={"vocabulary_id": content.vocab_a[1], "quality": 4})
    assert res.status_code == 200
    assert res.json() == {"next_review": _iso(1), "interval_days": 1}
    card = (await db.execute(select(models.SRSCard).where(
        models.SRSCard.student_id == student.id))).scalar_one()
    assert (card.repetitions, card.interval_days) == (1, 1)


async def test_reviewing_an_unknown_word_is_404(client, register):
    student = await register()
    res = await client.post("/api/me/srs/review", headers=student.headers,
                            json={"vocabulary_id": 99999, "quality": 4})
    assert res.status_code == 404


def test_preview_lists_the_interval_of_every_rating():
    assert preview_intervals(0, 2.5, 1) == {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}      # new card
    assert preview_intervals(1, 2.5, 1) == {0: 1, 1: 1, 2: 1, 3: 6, 4: 6, 5: 6}      # second review
    assert preview_intervals(2, 2.5, 6) == {0: 1, 1: 1, 2: 1, 3: 15, 4: 15, 5: 15}   # later reviews
    assert preview_intervals(4, 1.3, 20)[5] == 26


async def test_due_cards_say_what_each_rating_will_do(client, register, content):
    student = await register()
    await client.post(f"/api/me/srs/add-unit/{content.unit_a}", headers=student.headers)
    word = content.vocab_a[0]

    card = next(c for c in (await client.get("/api/me/srs/due", headers=student.headers)).json()
                if c["vocabulary_id"] == word)
    assert card["next_interval_days"] == {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1, "5": 1}

    # The preview is exactly what a review then does.
    await client.post("/api/me/srs/review", headers=student.headers,
                      json={"vocabulary_id": word, "quality": 4})
    from ._app import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        stored = (await db.execute(select(models.SRSCard).where(
            models.SRSCard.student_id == student.id, models.SRSCard.vocabulary_id == word))).scalar_one()
    expected = preview_intervals(stored.repetitions, stored.ease_factor, stored.interval_days)
    assert expected[4] == 6 and expected[1] == 1
