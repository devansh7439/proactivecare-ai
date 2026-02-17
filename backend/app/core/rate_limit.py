from __future__ import annotations

from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status

from app.core.config import settings


class InMemoryRateLimiter:
    def __init__(self, limit_per_minute: int) -> None:
        self.limit_per_minute = limit_per_minute
        self.requests: dict[str, deque[datetime]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = datetime.now(UTC)
        window_start = now - timedelta(minutes=1)
        queue = self.requests[key]

        while queue and queue[0] < window_start:
            queue.popleft()

        if len(queue) >= self.limit_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {self.limit_per_minute} prediction requests per minute.",
            )

        queue.append(now)


rate_limiter = InMemoryRateLimiter(settings.rate_limit_per_minute)
