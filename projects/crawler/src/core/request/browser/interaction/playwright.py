import asyncio
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

@dataclass(slots=True)
class BrowserInteractionExecution:

    phase: BrowserInteractionPhase = (
        BrowserInteractionPhase.INITIALIZING
    )

    transitions: list[
        BrowserInteractionPhase
    ] = field(
        default_factory=lambda: [
            BrowserInteractionPhase.INITIALIZING,
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
        self.transitions.append(phase)
        
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
        runtime_state = context.session_runtime.page_state
        phase = BrowserInteractionPhase.INITIALIZING
        await self._inspector.inspect(
            page,
            phase,
            runtime_state,
        )       
        for index, action in enumerate(
            context.config.actions,
            start=1,
        ):
            phase = BrowserInteractionPhase.INTERACTING            
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
            inspection = await self._inspector.inspect(
                page=page,
                phase=phase,
                runtime_state=runtime_state,
            )
            if inspection.state in {
                BrowserPageState.CHALLENGE,
                BrowserPageState.CAPTCHA,
            }:

                phase = (
                    BrowserInteractionPhase.HUMAN_INTERVENTION
                )

                intervention = (
                    self._interventions.resolve(
                        inspection.state,
                    )
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

                phase = (
                    BrowserInteractionPhase.RECOVERY
                )

                await self._wait_until_recovered(
                    page=page,
                    phase=phase,
                    runtime_state=runtime_state,
                )

        phase = BrowserInteractionPhase.COMPLETED

        logger.info(
            "[BrowserInteraction] completed",
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


    async def _wait_until_recovered(
        self,
        page: Page,
        phase: BrowserInteractionPhase,
        runtime_state: BrowserPageRuntimeState,
    ) -> None:

        deadline = (
            asyncio.get_running_loop().time()
            + self.RECOVERY_TIMEOUT
        )

        while True:

            await self._stabilizer.stabilize(
                page=page,
                phase=phase,
                runtime_state=runtime_state,
            )

            inspection = await self._inspector.inspect(
                page=page,
                phase=phase,
                runtime_state=runtime_state,
            )

            if inspection.state == BrowserPageState.NORMAL:
                logger.info(
                    "[BrowserRecovery] "
                    "page recovered.",
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