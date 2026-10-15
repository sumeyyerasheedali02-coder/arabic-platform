"""The Arabic tutor: prompt construction and the call to Google Gemini."""
import asyncio
import logging
import time
from typing import Sequence

from google import genai
from google.genai import types as genai_types

from app.config import get_settings
from app.schemas import ChatMessage

settings = get_settings()
logger = logging.getLogger(__name__)

_client = None

UNIT_VOCABULARY_LIMIT = 30
# Keep a small recent context even when older clients send their full history.
MAX_HISTORY_MESSAGES = 8
MAX_HISTORY_CHARACTERS = 6000


class TutorUnavailable(Exception):
    """The tutor could not answer. `reason` is safe to show to the student."""

    def __init__(self, reason: str, status_code: int = 503):
        super().__init__(reason)
        self.reason = reason
        self.status_code = status_code


def get_client():
    """Create the provider client on first use (tests replace this function)."""
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.google_api_key,
                               http_options=genai_types.HttpOptions(
                                   timeout=20000, retry_options=genai_types.HttpRetryOptions(attempts=1)))
    return _client


def build_unit_context(title_ar: str, title_tr: str, words: Sequence[str]) -> str:
    vocab_list = "، ".join(words)
    return f"""
الوحدة الحالية: {title_ar} ({title_tr})
المفردات المستهدفة في هذه الوحدة: {vocab_list}
استخدم هذه المفردات عندما تناسب السؤال، دون إقحامها أو إطالة الرد.
"""


def build_system_prompt(unit_context: str = "") -> str:
    return f"""أنت مرشد لتعلّم العربية للمبتدئين الأتراك.
المحادثة متاحة بالعربية والتركية. أجب بلغة سؤال الطالب الأخير أو اللغة المطلوبة صراحةً؛
للسؤال المختلط اتبع اللغة الغالبة. استخدم العربية الفصحى البسيطة أو التركية اليومية السهلة.
أجب مباشرة بأقل كلمات تكفي، غالبًا جملة أو جملتين. لا مقدمات أو مدح أو حشو أو تمرين أو سؤال متابعة تلقائي.
مثال قصير واحد عند طلبه أو الحاجة للفهم فقط؛ لا تضفه لكل رد. صحح الخطأ المقصود باختصار ولطف.
لا تكرر الإجابة باللغتين إلا بطلب. للتفصيل المطلوب أعطِ القدر الضروري فقط.
{unit_context}"""


def reply_config() -> genai_types.GenerateContentConfig:
    config = genai_types.GenerateContentConfig(
        temperature=0.5, max_output_tokens=256,
    )
    # Gemini 3 Flash supports minimal; 2.5 Flash supports disabling thinking.
    model = settings.gemini_model
    if model.startswith("gemini-3") and "flash" in model:
        config.thinking_config = genai_types.ThinkingConfig(thinking_level="minimal")
    elif model.startswith("gemini-2.5-flash"):
        config.thinking_config = genai_types.ThinkingConfig(thinking_budget=0)
    return config


def request_contents(messages: Sequence[ChatMessage]):
    selected = []
    characters = 0
    for message in reversed(messages[-MAX_HISTORY_MESSAGES:]):
        # Always preserve the latest question in full; drop older turns whole.
        if selected and characters + len(message.content) > MAX_HISTORY_CHARACTERS:
            break
        selected.append(message)
        characters += len(message.content)
    return [genai_types.Content(
        role="user" if message.role == "user" else "model",
        parts=[genai_types.Part(text=message.content)],
    ) for message in reversed(selected)]


async def generate_reply(messages: Sequence[ChatMessage], unit_context: str = "") -> str:
    """Send the conversation to the model and return its reply text.

    Raises TutorUnavailable when there is no usable answer; provider errors are
    logged here and never passed on to the caller.
    """
    if not settings.google_api_key:
        raise TutorUnavailable("المساعد الذكي غير مفعّل على هذا الخادم")

    config = reply_config()
    config.system_instruction = build_system_prompt(unit_context)
    try:
        response = await get_client().aio.models.generate_content(
            model=settings.gemini_model,
            contents=request_contents(messages), config=config,
        )
        reply = (response.text or "").strip()
    except Exception:
        logger.exception("The tutor request to the AI provider failed")
        raise TutorUnavailable("المساعد الذكي غير متاح حالياً، حاول بعد قليل") from None

    if not reply:
        # e.g. the provider withheld the answer
        raise TutorUnavailable("لم يصل رد من المساعد، حاول صياغة رسالتك بشكل آخر", status_code=502)
    return reply


async def stream_reply(messages: Sequence[ChatMessage], unit_context: str = ""):
    if not settings.google_api_key:
        raise TutorUnavailable("المساعد الذكي غير مفعّل على هذا الخادم")
    config = reply_config()
    config.system_instruction = build_system_prompt(unit_context)
    received = False
    started = time.perf_counter()
    try:
        deadline = asyncio.get_running_loop().time() + 30
        response = await asyncio.wait_for(get_client().aio.models.generate_content_stream(
            model=settings.gemini_model, contents=request_contents(messages), config=config), timeout=20)
        try:
            while True:
                remaining = max(0.01, deadline - asyncio.get_running_loop().time())
                try:
                    chunk = await asyncio.wait_for(anext(response), timeout=remaining)
                except StopAsyncIteration:
                    break
                if chunk.text:
                    if not received:
                        logger.info("Tutor first text arrived in %.2fs", time.perf_counter() - started)
                    received = True
                    yield chunk.text
        finally:
            await response.aclose()
    except Exception:
        logger.exception("The streamed tutor request failed")
        raise TutorUnavailable("تأخر المساعد أو تعذّر الاتصال به، حاول مجددًا") from None
    if not received:
        raise TutorUnavailable("لم يصل رد من المساعد، حاول صياغة رسالتك بشكل آخر", status_code=502)
    logger.info("Tutor reply completed in %.2fs", time.perf_counter() - started)
