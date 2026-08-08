# core/event/policy.py

from __future__ import annotations

from dataclasses import dataclass

from .typing import DispatchMode


@dataclass(frozen=True, slots=True)
class EventDispatchPolicy:
    """
    Defines the execution semantics of event dispatching.

    Parameters
    ----------
    mode:
        Whether handlers execute sequentially or concurrently.

    stop_on_error:
        Whether a handler failure aborts the dispatch.
    """

    mode: DispatchMode = DispatchMode.SEQUENTIAL

    stop_on_error: bool = True