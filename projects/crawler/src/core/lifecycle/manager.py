from types import TracebackType
from typing import Iterable, Self
import asyncio

from core.lifecycle.errors import LifecycleError
from core.lifecycle.mode import StartMode, StopMode
from core.lifecycle.protocol import Lifecycle
from core.lifecycle.state import LifecycleState
from contextlib import AbstractAsyncContextManager


class LifecycleManager(
    Lifecycle,
    AbstractAsyncContextManager["LifecycleManager"],
):

    def __init__(
        self,
        *,
        lifecycles: Iterable[Lifecycle] = (),
        start_mode: StartMode = StartMode.SEQUENTIAL,
        stop_mode: StopMode = StopMode.REVERSE,
    ) -> None:

        self._lifecycles = list(lifecycles)

        self._start_mode = start_mode

        self._stop_mode = stop_mode

        self._state = LifecycleState.CREATED

        self._frozen = False

    @property
    def state(self) -> LifecycleState:
        return self._state


    @property
    def running(self) -> bool:
        return self._state is LifecycleState.RUNNING


    @property
    def started(self) -> bool:
        return self._state not in (
            LifecycleState.CREATED,
            LifecycleState.STOPPED,
        )

    def freeze(self) -> None:

        self._frozen = True

    def _ensure_mutable(self) -> None:

        if self._frozen:

            raise LifecycleError(
                "LifecycleManager is frozen."
            )

    def add(
        self,
        lifecycle: Lifecycle,
    ) -> None:

        self._ensure_mutable()

        self._lifecycles.append(lifecycle)


    def remove(
        self,
        lifecycle: Lifecycle,
    ) -> None:

        self._ensure_mutable()

        self._lifecycles.remove(lifecycle)


    def clear(self) -> None:

        self._ensure_mutable()

        self._lifecycles.clear()


    def contains(
        self,
        lifecycle: Lifecycle,
    ) -> bool:

        return lifecycle in self._lifecycles


    def lifecycles(
        self,
    ) -> tuple[Lifecycle, ...]:

        return tuple(self._lifecycles)

    async def start(self) -> None:

        if self.running:
            return

        if self._state is LifecycleState.STARTING:
            raise LifecycleError(
                "LifecycleManager is already starting."
            )

        self._state = LifecycleState.STARTING

        try:

            match self._start_mode:

                case StartMode.SEQUENTIAL:
                    await self._start_sequential()

                case StartMode.PARALLEL:
                    await self._start_parallel()

            self._state = LifecycleState.RUNNING

        except Exception:

            self._state = LifecycleState.FAILED

            raise

    async def _start_sequential(self) -> None:

        started: list[Lifecycle] = []

        try:

            for lifecycle in self._lifecycles:

                await lifecycle.start()

                started.append(lifecycle)

        except Exception:

            for lifecycle in reversed(started):

                try:
                    await lifecycle.stop()
                except Exception:
                    pass

            raise

    async def _start_parallel(self) -> None:

        await asyncio.gather(
            *(
                lifecycle.start()
                for lifecycle in self._lifecycles
            )
        )

    async def stop(self) -> None:

        if self._state in (
            LifecycleState.CREATED,
            LifecycleState.STOPPED,
        ):
            return

        self._state = LifecycleState.STOPPING

        try:

            match self._stop_mode:

                case StopMode.REVERSE:
                    await self._stop_reverse()

                case StopMode.PARALLEL:
                    await self._stop_parallel()

        finally:

            self._state = LifecycleState.STOPPED

    async def _stop_reverse(self) -> None:

        errors: list[Exception] = []

        for lifecycle in reversed(
            self._lifecycles,
        ):

            try:

                await lifecycle.stop()

            except Exception as exc:

                errors.append(exc)

        if errors:

            raise ExceptionGroup(
                "Failed to stop lifecycle.",
                errors,
            )

    async def _stop_parallel(self) -> None:

        results = await asyncio.gather(
            *(
                lifecycle.stop()
                for lifecycle in self._lifecycles
            ),
            return_exceptions=True,
        )

        errors = [
            exc
            for exc in results
            if isinstance(exc, Exception)
        ]

        if errors:

            raise ExceptionGroup(
                "Failed to stop lifecycle.",
                errors,
            )

    async def __aenter__(self) -> Self:

        await self.start()

        return self


    async def __aexit__(
        self,
        exc_type:type[BaseException] | None,
        exc:BaseException | None,
        tb:TracebackType | None,
    ):

        await self.stop()