"""AI tutor requests, always against the mocked provider."""
import dataclasses


async def test_chat_returns_the_provider_reply_for_guests(client, fake_ai):
    res = await client.post("/api/chat", json={
        "messages": [{"role": "user", "content": "السلام عليكم"}]})
    assert res.status_code == 200
    assert res.json() == {"reply": fake_ai.reply, "corrections": []}
    assert len(fake_ai.calls) == 1


async def test_chat_forwards_history_with_provider_roles(client, fake_ai):
    await client.post("/api/chat", json={"messages": [
        {"role": "model", "content": "أهلاً!"},
        {"role": "user", "content": "اسمي علي"},
        {"role": "assistant", "content": "مرحباً علي"},
        {"role": "user", "content": "كيف حالك؟"},
    ]})
    contents = fake_ai.calls[0].contents
    assert [c.role for c in contents] == ["model", "user", "model", "user"]
    assert contents[-1].parts[0].text == "كيف حالك؟"


async def test_chat_system_prompt_requires_arabic_and_adds_unit_vocabulary(client, fake_ai, content):
    await client.post("/api/chat", json={
        "unit_id": content.unit_a, "messages": [{"role": "user", "content": "مرحبا"}]})
    prompt = fake_ai.calls[0].config.system_instruction
    assert "العربية الفصحى" in prompt
    assert "التَّحِيَّة" in prompt and "كِتَاب" in prompt

    await client.post("/api/chat", json={"messages": [{"role": "user", "content": "مرحبا"}]})
    assert "كِتَاب" not in fake_ai.calls[1].config.system_instruction


async def test_chat_reports_provider_failure_as_service_error(client, fake_ai):
    fake_ai.error = RuntimeError("quota exceeded")
    res = await client.post("/api/chat", json={"messages": [{"role": "user", "content": "مرحبا"}]})
    assert res.status_code == 503
    assert "quota" not in res.text and res.json()["detail"]


async def test_chat_handles_an_empty_provider_reply(client, fake_ai):
    for empty in (None, "", "   "):
        fake_ai.reply = empty
        res = await client.post("/api/chat", json={"messages": [{"role": "user", "content": "مرحبا"}]})
        assert res.status_code == 502


async def test_chat_rejects_an_empty_conversation(client, fake_ai):
    res = await client.post("/api/chat", json={"messages": []})
    assert res.status_code == 422 and fake_ai.calls == []


async def test_chat_rejects_empty_and_oversized_messages(client, fake_ai):
    for content in ("", "س" * 4001):
        res = await client.post("/api/chat", json={"messages": [{"role": "user", "content": content}]})
        assert res.status_code == 422
    assert fake_ai.calls == []


async def test_chat_passes_on_only_the_recent_part_of_a_long_conversation(client, fake_ai):
    from ._app import ai_service

    history = [{"role": "user" if i % 2 == 0 else "model", "content": f"رسالة {i}"} for i in range(101)]
    res = await client.post("/api/chat", json={"messages": history})
    assert res.status_code == 200
    contents = fake_ai.calls[0].contents
    assert len(contents) == ai_service.MAX_HISTORY_MESSAGES
    assert contents[-1].parts[0].text == "رسالة 100"


async def test_chat_without_an_api_key_says_so_and_calls_nobody(client, fake_ai, monkeypatch):
    from ._app import ai_service

    monkeypatch.setattr(ai_service, "settings", dataclasses.replace(ai_service.settings, google_api_key=""))
    res = await client.post("/api/chat", json={"messages": [{"role": "user", "content": "مرحبا"}]})
    assert res.status_code == 503 and fake_ai.calls == []
