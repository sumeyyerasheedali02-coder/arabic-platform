"""The Arabic tutor: prompt construction and the call to Google Gemini."""
from typing import Optional, Sequence

from google import genai
from google.genai import types as genai_types

from app.config import get_settings
from app.schemas import ChatMessage

settings = get_settings()

_client = None

UNIT_VOCABULARY_LIMIT = 30


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


async def generate_reply(messages: Sequence[ChatMessage], unit_context: str = "") -> Optional[str]:
    """Send the whole conversation to the model and return its reply text."""
    contents = [
        genai_types.Content(
            # The provider only knows "user" and "model".
            role="user" if message.role == "user" else "model",
            parts=[genai_types.Part(text=message.content)],
        )
        for message in messages
    ]
    response = await get_client().aio.models.generate_content(
        model=settings.gemini_model,
        contents=contents,
        config=genai_types.GenerateContentConfig(
            system_instruction=build_system_prompt(unit_context),
            temperature=0.7,
        ),
    )
    return response.text
