"""
خوارزمية SM-2 للحفظ المتباعد (Spaced Repetition System)
مبنية على خوارزمية SuperMemo-2 الأصلية
"""
from datetime import date, timedelta
from dataclasses import dataclass


@dataclass
class SRSResult:
    interval_days: int
    ease_factor:   float
    repetitions:   int
    next_review:   str   # ISO date


def sm2(quality: int, repetitions: int, ease_factor: float, interval_days: int) -> SRSResult:
    """
    quality      : 0–5 (0=فشل تام، 3=صحيح بصعوبة، 5=ممتاز)
    repetitions  : عدد المراجعات الناجحة المتتالية
    ease_factor  : معامل السهولة (يبدأ من 2.5)
    interval_days: الفترة الحالية بالأيام
    """
    if quality < 3:
        # فشل — أعد من البداية
        repetitions  = 0
        interval_days = 1
    else:
        if repetitions == 0:
            interval_days = 1
        elif repetitions == 1:
            interval_days = 6
        else:
            interval_days = round(interval_days * ease_factor)
        repetitions += 1

    # تحديث معامل السهولة
    ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ease_factor = max(1.3, ease_factor)

    next_review = (date.today() + timedelta(days=interval_days)).isoformat()

    return SRSResult(
        interval_days=interval_days,
        ease_factor=round(ease_factor, 3),
        repetitions=repetitions,
        next_review=next_review,
    )


def get_due_cards(cards: list, today: str = None) -> list:
    """إرجاع البطاقات التي حان وقت مراجعتها"""
    if today is None:
        today = date.today().isoformat()
    return [c for c in cards if c.next_review <= today]
