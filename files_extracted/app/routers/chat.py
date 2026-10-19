"""Conversation with the Arabic tutor (open to guests)."""
import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Student, Unit, Vocabulary
from app.schemas import ChatRequest, ChatResponse
from app.security import get_optional_account
from app.services import ai
from app.services.rate_limit import SlidingWindow, known_client_ip

router = APIRouter(prefix="/api", tags=["chat"])

# Every message costs a provider call. Logged-in accounts are counted on their
# own. Guests are counted per address when the address is known (a campus may
# share one), and all guests together are capped as well.
_chat_requests = SlidingWindow(600)
CHAT_MESSAGES_PER_ACCOUNT = 40
CHAT_MESSAGES_PER_GUEST_ADDRESS = 20
CHAT_MESSAGES_ALL_GUESTS = 300


def limit_chat(request: Request, account: Optional[Student] = Depends(get_optional_account)) -> None:
    if account is not None:
        limits = [(f"account:{account.id}", CHAT_MESSAGES_PER_ACCOUNT)]
        detail = "أرسلت رسائل كثيرة. انتظر بضع دقائق ثم حاول مجددًا"
    else:
        limits = [("guests", CHAT_MESSAGES_ALL_GUESTS)]
        address = known_client_ip(request)
        if address:
            limits.append((f"ip:{address}", CHAT_MESSAGES_PER_GUEST_ADDRESS))
        detail = "أرسلت رسائل كثيرة. انتظر بضع دقائق، أو سجّل الدخول لمتابعة المحادثة"
    if any(_chat_requests.exceeded(key, limit) for key, limit in limits):
        raise HTTPException(status_code=429, detail=detail)
    for key, _ in limits:
        _chat_requests.record(key)


async def _unit_context(db: AsyncSession, unit_id: int) -> str:
    unit = (await db.execute(select(Unit).where(Unit.id == unit_id))).scalar_one_or_none()
    if not unit:
        return ""
    vocab_result = await db.execute(
        select(Vocabulary).where(Vocabulary.unit_id == unit_id).limit(ai.UNIT_VOCABULARY_LIMIT)
    )
    words = [v.word_ar for v in vocab_result.scalars().all()]
    return ai.build_unit_context(unit.title_ar, unit.title_tr, words)


@router.post("/chat", response_model=ChatResponse, dependencies=[Depends(limit_chat)])
async def chat_with_ai(data: ChatRequest, db: AsyncSession = Depends(get_db)):
    """The client sends the whole conversation each time; nothing is stored server-side."""
    unit_context = await _unit_context(db, data.unit_id) if data.unit_id else ""
    try:
        reply = await ai.generate_reply(data.messages, unit_context)
    except ai.TutorUnavailable as problem:
        raise HTTPException(status_code=problem.status_code, detail=problem.reason) from None
    return ChatResponse(reply=reply, corrections=[])


@router.post("/chat/stream", dependencies=[Depends(limit_chat)])
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
