from __future__ import annotations

from typing import Self

from .manager import LifecycleManager
from .mode import StartMode, StopMode
from .protocol import Lifecycle


class LifecycleBuilder:
    """
    LifecycleManager Builder.
    """

    def __init__(self) -> None:

        self._lifecycles: list[Lifecycle] = []

        self._start_mode = StartMode.SEQUENTIAL

        self._stop_mode = StopMode.REVERSE

    def add(
        self,
        lifecycle: Lifecycle,
    ) -> Self:

        self._lifecycles.append(lifecycle)

        return self

    def remove(
        self,
        lifecycle: Lifecycle,
    ) -> Self:

        self._lifecycles.remove(lifecycle)

        return self

    def clear(self) -> Self:

        self._lifecycles.clear()

        return self

    def sequential(self) -> Self:

        self._start_mode = StartMode.SEQUENTIAL

        return self

    def parallel(self) -> Self:

        self._start_mode = StartMode.PARALLEL

        return self

    def reverse_stop(self) -> Self:

        self._stop_mode = StopMode.REVERSE

        return self

    def parallel_stop(self) -> Self:

        self._stop_mode = StopMode.PARALLEL

        return self

    def build(self) -> LifecycleManager:

        manager = LifecycleManager(
            lifecycles=self._lifecycles,
            start_mode=self._start_mode,
            stop_mode=self._stop_mode,
        )

        manager.freeze()

        return manager