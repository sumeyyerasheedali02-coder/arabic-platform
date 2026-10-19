"""Guest browsing: every content endpoint is public and read-only."""


async def test_root_reports_service(client):
    res = await client.get("/")
    assert res.status_code == 200 and "version" in res.json()


async def test_units_are_listed_in_unit_number_order(client, content):
    units = (await client.get("/api/units")).json()
    assert [u["unit_number"] for u in units] == [1, 2]
    assert units[0]["id"] == content.unit_a
    assert units[0]["title_tr"] == "Selamlama" and units[0]["total_lessons"] == 3


async def test_single_unit_and_missing_unit(client, content):
    assert (await client.get(f"/api/units/{content.unit_a}")).json()["title_ar"] == "التَّحِيَّة"
    assert (await client.get("/api/units/99999")).status_code == 404


async def test_lessons_of_unit_are_ordered(client, content):
    lessons = (await client.get(f"/api/units/{content.unit_a}/lessons")).json()
    assert [(item["lesson_number"], item["lesson_type"]) for item in lessons] == [
        (1, "hiwar"), (2, "mufradat"), (3, "nahw")]
    assert lessons[2]["grammar_focus"] == "قاعدة أولى | قاعدة ثانية"


async def test_single_lesson_and_missing_lesson(client, content):
    lesson = (await client.get(f"/api/lessons/{content.a_muf}")).json()
    assert lesson["id"] == content.a_muf and lesson["title_tr"] == "Kelimeler"
    # A lesson says which unit it belongs to, so a page can load its unit's vocabulary
    assert lesson["unit_id"] == content.unit_a and lesson["content_ar"] is None
    assert (await client.get("/api/lessons/99999")).status_code == 404


async def test_unit_vocabulary_carries_translations_and_lesson(client, content):
    vocab = (await client.get(f"/api/units/{content.unit_a}/vocabulary")).json()
    assert [v["id"] for v in vocab] == content.vocab_a
    first = vocab[0]
    assert (first["word_ar"], first["translation_tr"], first["translation_en"]) == ("كِتَاب", "kitap", "book")
    assert first["lesson_id"] == content.a_muf


async def test_vocabulary_search_matches_arabic_and_turkish(client):
    by_tr = (await client.get("/api/vocabulary/search", params={"q": "kalem"})).json()
    by_ar = (await client.get("/api/vocabulary/search", params={"q": "بَيْت"})).json()
    assert [v["word_ar"] for v in by_tr] == ["قَلَم"]
    assert [v["translation_tr"] for v in by_ar] == ["ev"]


async def test_dialogues_return_lines_in_order(client, content):
    dialogues = (await client.get(f"/api/lessons/{content.a_hiwar}/dialogues")).json()
    assert len(dialogues) == 1
    assert [line["line_order"] for line in dialogues[0]["lines"]] == [1, 2]
    assert dialogues[0]["lines"][0]["speaker"] == "خالد"
    assert (await client.get(f"/api/lessons/{content.a_muf}/dialogues")).json() == []


async def test_dialogue_audio_uses_content_numbers_not_database_ids(client, content, monkeypatch):
    from content.dialogue_audio import DIALOGUE_AUDIO

    # The fixture inserts unit 2 before unit 1, so their row IDs and numbers differ.
    assert content.unit_a != 1
    monkeypatch.setitem(DIALOGUE_AUDIO, (1, 1), "https://media.example.test/unit-01/dialogue-01.mp3")
    monkeypatch.setitem(DIALOGUE_AUDIO, (content.unit_a, 1), "https://media.example.test/wrong-unit.mp3")
    dialogues = (await client.get(f"/api/lessons/{content.a_hiwar}/dialogues")).json()
    assert dialogues[0]["audio_url"] == "https://media.example.test/unit-01/dialogue-01.mp3"
    assert dialogues[0]["audio_is_partial"] is False
    assert len(dialogues[0]["lines"]) == 2


async def test_dialogue_without_published_recording_has_no_audio(client, content, monkeypatch):
    from content.dialogue_audio import DIALOGUE_AUDIO

    monkeypatch.delitem(DIALOGUE_AUDIO, (1, 1))
    dialogues = (await client.get(f"/api/lessons/{content.a_hiwar}/dialogues")).json()
    assert dialogues[0]["audio_url"] is None


async def test_incomplete_recording_is_labelled_without_truncating_lesson_text(client, content, monkeypatch):
    from content.dialogue_audio import DIALOGUE_AUDIO

    from ._app import AsyncSessionLocal, models

    monkeypatch.setitem(DIALOGUE_AUDIO, (2, 2), "https://media.example.test/partial.mp3")
    async with AsyncSessionLocal() as db:
        dialogue = models.Dialogue(lesson_id=content.b_hiwar, dialogue_number=2, title_ar="الحوار الثاني")
        db.add(dialogue)
        await db.flush()
        db.add_all([
            models.DialogueLine(dialogue_id=dialogue.id, line_order=1, speaker="عمر", text_ar="وهذا عمه حمزة"),
            models.DialogueLine(dialogue_id=dialogue.id, line_order=2, speaker="عثمان", text_ar="وهذا عمه أبو طالب"),
        ])
        await db.commit()
    dialogues = (await client.get(f"/api/lessons/{content.b_hiwar}/dialogues")).json()
    assert dialogues[0]["audio_url"] == "https://media.example.test/partial.mp3"
    assert dialogues[0]["audio_is_partial"] is True
    assert [line["text_ar"] for line in dialogues[0]["lines"]] == ["وهذا عمه حمزة", "وهذا عمه أبو طالب"]


async def test_exercises_are_listed_and_filterable(client, content):
    url = f"/api/units/{content.unit_a}/exercises"
    everything = (await client.get(url)).json()
    assert [e["exercise_number"] for e in everything] == [1, 2, 3, 4, 5]
    assert everything[0]["options"] == ["kalem", "kitap", "ev", "okul"]
    # Guests check their answers locally, so the answer is part of the public payload.
    assert everything[0]["correct_answer"] == "kitap"

    blanks = (await client.get(url, params={"ex_type": "fill_blank"})).json()
    assert {e["id"] for e in blanks} == {content.ex_blank, content.ex_order}
    hard = (await client.get(url, params={"difficulty": 3})).json()
    assert {e["id"] for e in hard} == {content.ex_synonym, content.ex_order}

    categories = {e["id"]: e["category"] for e in everything}
    assert categories == {content.ex_choice: None, content.ex_true_false: None, content.ex_blank: None,
                          content.ex_synonym: "synonym", content.ex_order: "word_order"}
