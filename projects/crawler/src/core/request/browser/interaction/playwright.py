import asyncio
from typing import Any
from dataclasses import dataclass, field
from playwright.async_api import Page
import logging

from core.request.browser.executor.registry import BrowserActionExecutorRegistry
from core.request.browser.interaction.model import BrowserAction
from core.request.browser.intervention.registry import HumanInterventionEngineRegistry
from core.request.browser.snapshot import BrowserPageRuntimeState
from core.request.browser.stabilizer.base import BrowserPageStabilizer
from core.request.browser.typing import BrowserInteractionPhase, BrowserPageState
from core.request.browser.inspector.base import (
    BrowserPageInspector,
)
from core.request.browser.interaction.base import (
    BrowserInteractionEngine,
)
from core.request.browser.interaction.context import (
    BrowserInteractionContext,
)
from core.spider.config import SearchSpiderConfig
from core.request.browser.inspector.model import BrowserPageInspection

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
        
class PlaywrightBrowserInteractionEngine(
    BrowserInteractionEngine,
):
    """
    Execute browser interaction actions against a
    Playwright page.

    Responsibilities:
    - dispatch BrowserAction
    - execute browser actions
    - inspect page state after actions
    - resolve optional human intervention
    - wait for page recovery

    This engine does not own:
    - Browser
    - BrowserContext
    - Page lifecycle
    - Request lifecycle
    - Cookie lifecycle
    """

    RECOVERY_TIMEOUT = 120.0
    RECOVERY_INTERVAL = 1.0

    def __init__(
        self,
        inspector: BrowserPageInspector,
        stabilizer: BrowserPageStabilizer,
        human_intervention_registry: HumanInterventionEngineRegistry,
        executor_registry: BrowserActionExecutorRegistry,
    ) -> None:

        self._inspector = inspector
        self._stabilizer = stabilizer
        self._interventions = human_intervention_registry
        self._executors = executor_registry

    async def execute(
        self,
        context: BrowserInteractionContext[
            SearchSpiderConfig
        ],
    ) -> None:

        page = context.session_runtime.page

        runtime_state = (
            context.session_runtime.page_state
        )

        execution = (
            BrowserInteractionExecution()
        )

        try:

            await self._initialize(
                page=page,
                runtime_state=runtime_state,
                execution=execution,
            )

            for index, action in enumerate(
                context.config.actions,
                start=1,
            ):
                await self._process_action(
                    context=context,
                    page=page,
                    runtime_state=runtime_state,
                    execution=execution,
                    index=index,
                    action=action,
                )

            self._transition_to(
                execution,
                BrowserInteractionPhase.COMPLETED,
            )

            logger.info(
                "[BrowserInteraction] completed "
                "transitions=%s",
                self._format_transitions(
                    execution,
                ),
            )

        except Exception:
            logger.exception(
                "[BrowserInteraction] failed "
                "phase=%s",
                execution.phase.value,
            )
            raise

    async def _initialize(
        self,
        *,
        page: Page,
        runtime_state: BrowserPageRuntimeState,
        execution: BrowserInteractionExecution,
    ) -> BrowserPageInspection:

        self._transition_to(
            execution,
            BrowserInteractionPhase.INITIALIZING,
        )

        return await self._inspect(
            page=page,
            runtime_state=runtime_state,
            execution=execution,
        )

    async def _process_action(
        self,
        *,
        context: BrowserInteractionContext[
            SearchSpiderConfig
        ],
        page: Page,
        runtime_state: BrowserPageRuntimeState,
        execution: BrowserInteractionExecution,
        index: int,
        action: BrowserAction,
    ) -> None:

        self._transition_to(
            execution,
            BrowserInteractionPhase.INTERACTING,
        )

        logger.info(
            "[BrowserAction] #%d type=%s",
            index,
            action.type,
        )

        await self._execute_action(
            page=page,
            action=action,
        )

        logger.info(
            "[BrowserAction] #%d completed",
            index,
        )

        inspection = await self._inspect(
            page=page,
            runtime_state=runtime_state,
            execution=execution,
        )

        if inspection.state in {
            BrowserPageState.CHALLENGE,
            BrowserPageState.CAPTCHA,
        }:
            await self._handle_intervention(
                context=context,
                page=page,
                runtime_state=runtime_state,
                execution=execution,
                inspection=inspection,
            )

    async def _handle_intervention(
        self,
        *,
        context: BrowserInteractionContext[Any],
        page: Page,
        runtime_state: BrowserPageRuntimeState,
        execution: BrowserInteractionExecution,
        inspection: BrowserPageInspection,
    ) -> None:

        self._transition_to(
            execution,
            BrowserInteractionPhase.HUMAN_INTERVENTION,
        )

        intervention = self._interventions.resolve(
            inspection.state,
        )

        if intervention is None:
            raise RuntimeError(
                "No human intervention engine is "
                f"registered for state "
                f"{inspection.state!r}.",
            )

        logger.info(
            "[BrowserIntervention] "
            "engine=%s state=%s",
            type(intervention).__name__,
            inspection.state.value,
        )

        await intervention.intervene(
            context,
            inspection,
        )

        await self._recover(
            page=page,
            runtime_state=runtime_state,
            execution=execution,
        )

    async def _recover(
        self,
        *,
        page: Page,
        runtime_state: BrowserPageRuntimeState,
        execution: BrowserInteractionExecution,
    ) -> None:

        self._transition_to(
            execution,
            BrowserInteractionPhase.RECOVERY,
        )

        deadline = (
            asyncio.get_running_loop().time()
            + self.RECOVERY_TIMEOUT
        )

        while True:

            await self._stabilizer.stabilize(
                page=page,
                phase=execution.phase,
                runtime_state=runtime_state,
            )

            inspection = await self._inspect(
                page=page,
                runtime_state=runtime_state,
                execution=execution,
            )

            if inspection.state == (
                BrowserPageState.NORMAL
            ):
                logger.info(
                    "[BrowserRecovery] "
                    "page recovered.",
                )

                self._transition_to(
                    execution,
                    BrowserInteractionPhase.INTERACTING,
                )

                return

            if (
                asyncio.get_running_loop().time()
                >= deadline
            ):
                raise TimeoutError(
                    "Browser page did not recover "
                    "after human intervention.",
                )

            await asyncio.sleep(
                self.RECOVERY_INTERVAL,
            )

    async def _inspect(
        self,
        *,
        page: Page,
        runtime_state: BrowserPageRuntimeState,
        execution: BrowserInteractionExecution,
    ) -> BrowserPageInspection:

        return await self._inspector.inspect(
            page=page,
            phase=execution.phase,
            runtime_state=runtime_state,
        )

    def _transition_to(
        self,
        execution: BrowserInteractionExecution,
        phase: BrowserInteractionPhase,
    ) -> None:

        previous = execution.phase

        execution.transition_to(
            phase,
        )

        if previous == execution.phase:
            return

        logger.info(
            "[BrowserInteractionPhase] "
            "%s -> %s",
            previous.value,
            execution.phase.value,
        )

    async def _execute_action(
        self,
        *,
        page: Page,
        action: BrowserAction,
    ) -> None:

        executor = self._executors.resolve(
            action.type,
        )

        await executor.execute(
            page,
            action,
        )

    @staticmethod
    def _format_transitions(
        execution: BrowserInteractionExecution,
    ) -> str:

        transitions = execution.transitions

        if not transitions:
            return "<none>"

        phases = [
            transition.to_phase
            for transition in transitions
        ]

        return " -> ".join(phases)