from __future__ import annotations

import json
import time
from typing import Any, Callable

import httpx


def run_with_retry(
    fn: Callable[[], Any],
    *,
    retries: int = 3,
    delay_seconds: float = 1.0,
) -> Any:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            return fn()
        except Exception as exc:  # pragma: no cover - defensive branch
            last_error = exc
            if attempt < retries - 1:
                time.sleep(delay_seconds)
                continue
    if last_error is not None:
        raise last_error
    raise RuntimeError("retry operation failed")


def post_with_retry(url: str, payload: dict[str, Any], *, retries: int = 3) -> dict[str, Any]:
    def _request() -> dict[str, Any]:
        response = httpx.post(url, json=payload, timeout=10.0)
        response.raise_for_status()
        return response.json() if response.content else {}

    return run_with_retry(_request, retries=retries)
