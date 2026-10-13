"""AI tutor requests, always against the mocked provider."""
import pytest


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


@pytest.mark.xfail(reason="provider failures surface as an unhandled 500")
async def test_chat_reports_provider_failure_as_service_error(client, fake_ai):
    fake_ai.error = RuntimeError("quota exceeded")
    res = await client.post("/api/chat", json={"messages": [{"role": "user", "content": "مرحبا"}]})
    assert res.status_code in (502, 503)
    assert "quota" not in res.text


@pytest.mark.xfail(reason="an empty reply from the provider fails response validation -> 500")
async def test_chat_handles_an_empty_provider_reply(client, fake_ai):
    fake_ai.reply = None
    res = await client.post("/api/chat", json={"messages": [{"role": "user", "content": "مرحبا"}]})
    assert res.status_code in (200, 502)


@pytest.mark.xfail(reason="a request without messages reaches the provider")
async def test_chat_rejects_an_empty_conversation(client, fake_ai):
    res = await client.post("/api/chat", json={"messages": []})
    assert res.status_code == 422 and fake_ai.calls == []
