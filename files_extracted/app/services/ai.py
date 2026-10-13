"""The Arabic tutor: prompt construction and the call to Google Gemini."""
import logging
from typing import Sequence

from google import genai
from google.genai import types as genai_types

from app.config import get_settings
from app.schemas import ChatMessage

settings = get_settings()
logger = logging.getLogger(__name__)

_client = None

UNIT_VOCABULARY_LIMIT = 30
# The client resends the whole conversation with every message. Only the most
# recent part is passed on, so a long chat cannot grow the request without limit.
MAX_HISTORY_MESSAGES = 40


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
        _client = genai.Client(api_key=settings.google_api_key)
    return _client


def build_unit_context(title_ar: str, title_tr: str, words: Sequence[str]) -> str:
    vocab_list = "، ".join(words)
    return f"""
الوحدة الحالية: {title_ar} ({title_tr})
المفردات المستهدفة في هذه الوحدة: {vocab_list}
استخدم هذه المفردات في ردودك قدر الإمكان.
"""


def build_system_prompt(unit_context: str = "") -> str:
    return f"""أنت مساعد لتعليم اللغة العربية لطالب تركي يدرس في كلية الإلهيات.

قواعد صارمة:
1. تحدث بالعربية الفصحى فقط في جميع ردودك
2. إذا أخطأ الطالب في الإعراب أو المفردات، صحح الخطأ بلطف
3. استخدم جملاً بسيطة ومفهومة تناسب المستوى الأول
4. إذا كتب الطالب بالتركية، رد عليه بالعربية وأخبره بلطف أن يحاول بالعربية
5. شجع الطالب وكن إيجابياً دائماً
6. في نهاية كل رد، اقترح جملة تدريبية واحدة للطالب

{unit_context}

تذكر: هدفك هو مساعدة الطالب على التواصل بالعربية بشكل طبيعي."""


async def generate_reply(messages: Sequence[ChatMessage], unit_context: str = "") -> str:
    """Send the conversation to the model and return its reply text.

    Raises TutorUnavailable when there is no usable answer; provider errors are
    logged here and never passed on to the caller.
    """
    if not settings.google_api_key:
        raise TutorUnavailable("المساعد الذكي غير مفعّل على هذا الخادم")

    contents = [
        genai_types.Content(
            # The provider only knows "user" and "model".
            role="user" if message.role == "user" else "model",
            parts=[genai_types.Part(text=message.content)],
        )
        for message in messages[-MAX_HISTORY_MESSAGES:]
    ]
    try:
        response = await get_client().aio.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=genai_types.GenerateContentConfig(
                system_instruction=build_system_prompt(unit_context),
                temperature=0.7,
            ),
        )
        reply = (response.text or "").strip()
    except Exception:
        logger.exception("The tutor request to the AI provider failed")
        raise TutorUnavailable("المساعد الذكي غير متاح حالياً، حاول بعد قليل") from None

    if not reply:
        # e.g. the provider withheld the answer
        raise TutorUnavailable("لم يصل رد من المساعد، حاول صياغة رسالتك بشكل آخر", status_code=502)
    return reply
