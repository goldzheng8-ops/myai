import asyncio
import time
from dataclasses import dataclass
from typing import Protocol

class ThrottleLimiter(Protocol):
    """
    Coordinate request execution for a throttling scope.

    A limiter controls when a request is allowed to start
    and releases the execution slot after the request finishes.
    """

    async def acquire(
        self,
        key: str,
    ) -> None:
        """
        Wait until the request is allowed to execute.
        """
        ...

    def release(
        self,
        key: str,
    ) -> None:
        """
        Release the execution slot for the given key.
        """
        ...

@dataclass(slots=True)
class _ThrottleState:

    lock: asyncio.Lock

    semaphore: asyncio.Semaphore | None

    last_acquired: float = 0.0

class InMemoryThrottleLimiter:

    def __init__(
        self,
        *,
        delay: float = 0.0,
        concurrency: int | None = None,
    ) -> None:

        if delay < 0:
            raise ValueError(
                "delay must be >= 0."
            )

        if (
            concurrency is not None
            and concurrency <= 0
        ):
            raise ValueError(
                "concurrency must be > 0."
            )

        self._delay = delay
        self._concurrency = concurrency

        self._states: dict[
            str,
            _ThrottleState,
        ] = {}

        self._states_lock = asyncio.Lock()

    async def _get_state(
        self,
        key: str,
    ) -> _ThrottleState:

        async with self._states_lock:

            state = self._states.get(key)

            if state is not None:
                return state

            semaphore = None

            if self._concurrency is not None:
                semaphore = asyncio.Semaphore(
                    self._concurrency,
                )

            state = _ThrottleState(
                lock=asyncio.Lock(),
                semaphore=semaphore,
            )

            self._states[key] = state

            return state

    async def acquire(
        self,
        key: str,
    ) -> None:

        state = await self._get_state(
            key,
        )

        if state.semaphore is not None:
            await state.semaphore.acquire()

        async with state.lock:

            now = time.monotonic()

            elapsed = (
                now - state.last_acquired
            )

            wait = self._delay - elapsed

            if wait > 0:
                await asyncio.sleep(wait)

            state.last_acquired = (
                time.monotonic()
            )

    def release(
        self,
        key: str,
    ) -> None:

        state = self._states.get(key)

        if state is None:
            return

        if state.semaphore is not None:
            state.semaphore.release()