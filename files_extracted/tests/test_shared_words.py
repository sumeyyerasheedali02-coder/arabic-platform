"""The shared Arabic–Turkish vocabulary endpoint (public, served from content)."""
from content.shared_words import CATEGORIES, all_words


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
