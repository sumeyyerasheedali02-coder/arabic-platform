"""In-process sliding-window request limits.

Counts live in this process only: they reset when the server restarts and are
not shared between replicas. That is enough to stop one client from guessing
passwords or spending the tutor's quota; it is not a gateway-level limit.
"""
import hashlib
import time
from collections import OrderedDict

from fastapi import Request

from app.config import get_settings

MAX_KEYS = 10000
_limiters: list["SlidingWindow"] = []


def _digest(key: str) -> str:
    # Keys contain e-mail addresses and IPs; keep only their hashes in memory.
    return hashlib.sha256(key.encode()).hexdigest()


class SlidingWindow:
    def __init__(self, window_seconds: int):
        self.window = window_seconds
        self._hits: OrderedDict[str, list[float]] = OrderedDict()
        _limiters.append(self)

    def _recent(self, digest: str, now: float) -> list[float]:
        return [stamp for stamp in self._hits.get(digest, []) if now - stamp < self.window]

    def exceeded(self, key: str, limit: int) -> bool:
        return len(self._recent(_digest(key), time.monotonic())) >= limit

    def record(self, key: str) -> None:
        digest, now = _digest(key), time.monotonic()
        self._hits[digest] = self._recent(digest, now) + [now]
        self._hits.move_to_end(digest)
        while len(self._hits) > MAX_KEYS:
            self._hits.popitem(last=False)

    def clear(self) -> None:
        self._hits.clear()


def client_ip(request: Request) -> str:
    """The caller's address.

    Behind a proxy every request comes from the proxy, so the address is taken
    from the header named by CLIENT_IP_HEADER when it is configured. Only name a
    header that the proxy sets itself; a client can send any header it likes.
    For a list (X-Forwarded-For) the last entry is the one the proxy appended.
    """
    header = get_settings().client_ip_header
    if header:
        value = request.headers.get(header, "").split(",")[-1].strip()
        if value:
            return value
    return request.client.host if request.client else "unknown"


def known_client_ip(request: Request) -> str | None:
    """The caller's address only when CLIENT_IP_HEADER says where to find it.

    Without it, every request behind the proxy shares the proxy's address, and
    a per-address limit would lock out everyone at once; such limits are then
    skipped (per-account limits still apply).
    """
    header = get_settings().client_ip_header
    value = request.headers.get(header, "").split(",")[-1].strip() if header else ""
    return value or None


def reset_all() -> None:
    """Forget every count (used by the tests)."""
    for limiter in _limiters:
        limiter.clear()
