"""The shared Arabic–Turkish vocabulary endpoint (public, served from content)."""
from content.shared_words import CATEGORIES, all_words
from content.unit_shared_words import UNIT_SHARED_WORDS


async def test_shared_words_are_public_and_grouped(client):
    res = await client.get("/api/shared-words")
    assert res.status_code == 200
    body = res.json()
    assert body["total"] == len(all_words())
    assert len(body["categories"]) == len(CATEGORIES)
    first = body["categories"][0]
    assert {"key", "title_ar", "words"} <= set(first)
    assert {"ar", "tr", "usage"} <= set(first["words"][0])


async def test_every_word_is_well_formed():
    for word in all_words():
        assert word["ar"].strip(), word
        assert word["tr"].strip(), word
        assert word["usage"] in ("شائعة", "تراثية"), word
        assert "note" in word


async def test_no_duplicate_arabic_turkish_pairs_within_a_category():
    for category in CATEGORIES:
        pairs = [(w["ar"], w["tr"]) for w in category["words"]]
        assert len(pairs) == len(set(pairs)), category["key"]


# ── the «كلمات مشتركة» tab of each unit ─────────────────────────────────────


async def test_every_platform_unit_has_shared_words():
    assert sorted(UNIT_SHARED_WORDS) == list(range(1, 49))
    for number, words in UNIT_SHARED_WORDS.items():
        assert len(words) >= 20, number


async def test_unit_words_come_from_the_audited_dataset():
    known = {(w["ar"], w["tr"]): w for w in all_words()}
    for number, words in UNIT_SHARED_WORDS.items():
        pairs = [(w["ar"], w["tr"]) for w in words]
        assert len(pairs) == len(set(pairs)), number
        for word in words:
            source = known[(word["ar"], word["tr"])]
            assert word["usage"] == source["usage"] and word["note"] == source["note"]


async def test_unit_shared_words_endpoint_is_public(client):
    res = await client.get("/api/shared-words/units/6")
    assert res.status_code == 200
    body = res.json()
    assert body["unit_number"] == 6 and body["total"] == len(body["words"])
    assert {"ar", "tr", "usage", "note"} <= set(body["words"][0])
    assert any(w["tr"] == "mescit" for w in body["words"])


async def test_unit_shared_words_unknown_unit_is_404(client):
    assert (await client.get("/api/shared-words/units/0")).status_code == 404
    assert (await client.get("/api/shared-words/units/49")).status_code == 404
