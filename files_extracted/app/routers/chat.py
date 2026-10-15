"""Conversation with the Arabic tutor (open to guests)."""
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Unit, Vocabulary
from app.schemas import ChatRequest, ChatResponse
from app.services import ai

router = APIRouter(prefix="/api", tags=["chat"])


async def _unit_context(db: AsyncSession, unit_id: int) -> str:
    unit = (await db.execute(select(Unit).where(Unit.id == unit_id))).scalar_one_or_none()
    if not unit:
        return ""
    vocab_result = await db.execute(
        select(Vocabulary).where(Vocabulary.unit_id == unit_id).limit(ai.UNIT_VOCABULARY_LIMIT)
    )
    words = [v.word_ar for v in vocab_result.scalars().all()]
    return ai.build_unit_context(unit.title_ar, unit.title_tr, words)


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(data: ChatRequest, db: AsyncSession = Depends(get_db)):
    """The client sends the whole conversation each time; nothing is stored server-side."""
    unit_context = await _unit_context(db, data.unit_id) if data.unit_id else ""
    try:
        reply = await ai.generate_reply(data.messages, unit_context)
    except ai.TutorUnavailable as problem:
        raise HTTPException(status_code=problem.status_code, detail=problem.reason) from None
    return ChatResponse(reply=reply, corrections=[])


@router.post("/chat/stream")
async def stream_chat(data: ChatRequest, db: AsyncSession = Depends(get_db)):
    unit_context = await _unit_context(db, data.unit_id) if data.unit_id else ""
    reply = ai.stream_reply(data.messages, unit_context)
    try:
        first = await anext(reply)
    except ai.TutorUnavailable as problem:
        raise HTTPException(status_code=problem.status_code, detail=problem.reason) from None

    def event(value):
        return json.dumps(value, ensure_ascii=False) + "\n"

    async def events():
        try:
            yield event({"text": first})
            async for text in reply:
                yield event({"text": text})
            yield event({"done": True})
        except ai.TutorUnavailable as problem:
            yield event({"error": problem.reason})
        finally:
            await reply.aclose()

    return StreamingResponse(events(), media_type="application/x-ndjson",
                             headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"})
