import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine
from playwright.async_api import Page, Response,BrowserContext

from core.request.browser.cookie_sink import BrowserCookieSink
from core.request.browser.snapshot import BrowserPageRuntimeState
from core.request.browser.typing import BrowserInteractionPhase
from core.request.middleware.proxy.config import ProxyConfig

logger=logging.getLogger(__name__)

_PHASE_TRANSITIONS: dict[
    BrowserInteractionPhase,
    frozenset[BrowserInteractionPhase],
] = {
    BrowserInteractionPhase.INITIALIZING: frozenset(
        {
            BrowserInteractionPhase.INTERACTING,
            BrowserInteractionPhase.COMPLETED,
        }
    ),

    BrowserInteractionPhase.INTERACTING: frozenset(
        {
            BrowserInteractionPhase.INTERACTING,
            BrowserInteractionPhase.HUMAN_INTERVENTION,
            BrowserInteractionPhase.COMPLETED,
        }
    ),

    BrowserInteractionPhase.HUMAN_INTERVENTION: frozenset(
        {
            BrowserInteractionPhase.RECOVERY,
        }
    ),

    BrowserInteractionPhase.RECOVERY: frozenset(
        {
            BrowserInteractionPhase.INTERACTING,
            BrowserInteractionPhase.COMPLETED,
        }
    ),

    BrowserInteractionPhase.COMPLETED: frozenset(),
}

@dataclass(frozen=True, slots=True)
class BrowserPhaseTransition:

    from_phase: BrowserInteractionPhase  = BrowserInteractionPhase.INITIALIZING
    to_phase: BrowserInteractionPhase  = BrowserInteractionPhase.INITIALIZING

@dataclass(slots=True)
class BrowserInteractionExecution:

    phase: BrowserInteractionPhase = (
        BrowserInteractionPhase.INITIALIZING
    )

    transitions: list[
        BrowserPhaseTransition
    ] = field(
        default_factory=lambda: [
            BrowserPhaseTransition(),
        ],
    )

    def transition_to(
        self,
        phase: BrowserInteractionPhase,
    ) -> None:

        current = self.phase

        if phase == current:
            return

        allowed = _PHASE_TRANSITIONS[current]

        if phase not in allowed:
            raise RuntimeError(
                "Invalid browser interaction phase "
                f"transition: "
                f"{current.value!r} -> "
                f"{phase.value!r}.",
            )

        self.phase = phase
        self.transitions.append(
            BrowserPhaseTransition(
                from_phase=current,
                to_phase=phase,
            )
        )


@dataclass(slots=True)
class BrowserSessionRuntime:
    session_id: str

    context: BrowserContext
    page: Page

    proxy: ProxyConfig | None = None

    cookie_sink: BrowserCookieSink | None = None

    page_state: BrowserPageRuntimeState = field(
        default_factory=BrowserPageRuntimeState,
    )

    lock: asyncio.Lock = field(
        default_factory=asyncio.Lock,
    )

    cookie_tasks: set[
        asyncio.Task[None]
    ] = field(
        default_factory=set,
    )

    debug_tasks: set[
        asyncio.Task[None]
    ] = field(
        default_factory=set,
    )
    response_handler: (
        Callable[[Response], None] | None
    ) = None

    async def close(self) -> None:

        if self.response_handler is not None:
            self.context.remove_listener(
                "response",
                self.response_handler,
            )

            self.response_handler = None

        tasks = tuple(self.cookie_tasks)

        self.cookie_tasks.clear()

        if tasks:
            await asyncio.gather(
                *tasks,
                return_exceptions=True,
            )

        if not self.page.is_closed():
            await self.page.close()

        await self.context.close()

    def create_debug_task(
        self,
        coroutine: Coroutine[Any, Any, None],
    ) -> None:

        task = asyncio.create_task(
            coroutine,
        )

        self.debug_tasks.add(task)

        task.add_done_callback(
            self._consume_debug_task,
        )

    def _consume_debug_task(
        self,
        task: asyncio.Task[None],
    ) -> None:

        self.debug_tasks.discard(task)

        if task.cancelled():
            return

        exception = task.exception()

        if exception is not None:
            logger.debug(
                "[BrowserDebug] "
                "debug task failed: %s",
                exception,
                exc_info=exception,
            )