import asyncio
from typing import Any

from core.request.browser.model import BrowserInteractionExecution
from core.request.browser.runtime_debugger import BrowserRuntimeDebugger
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
        debugger: BrowserRuntimeDebugger,
    ) -> None:

        self._inspector = inspector
        self._stabilizer = stabilizer
        self._interventions = human_intervention_registry
        self._executors = executor_registry
        self._debugger = debugger

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

            self._debugger.log_transitions(
                execution=execution,
            )

        except Exception as exc:
            self._debugger.log_interaction_failed(
                phase=execution.phase,
                exc=exc,
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
        context: BrowserInteractionContext[Any],
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

        self._debugger.log_action(
            index=index,
            action=action,
        )

        await self._execute_action(
            page=page,
            action=action,
            context=context,
        )

        self._debugger.log_action(
            index=index,
            action=action,
            completed=True,
        )

        inspection = await self._inspect(
            page=page,
            runtime_state=runtime_state,
            execution=execution,
        )

        if inspection.state in {
            BrowserPageState.CHALLENGE,
            BrowserPageState.CAPTCHA,
            # BrowserPageState.LOGIN_REQUIRED,
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

        self._debugger.log_intervention(
            engine=intervention,
            state=inspection.state,
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
                BrowserPageState.UNKNOWN
            ):
                self._debugger.log_recovery(
                    recovered=True,
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
            self._debugger.log_recovery(
                recovered=False,
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

        self._debugger.log_phase(
            previous=previous,
            current=execution.phase,
        )

    async def _execute_action(
        self,
        *,
        page: Page,
        action: BrowserAction,
        context: BrowserInteractionContext[Any],        
    ) -> None:

        executor = self._executors.resolve(
            action.type,
        )

        await executor.execute(
            page,
            action,
            context.request.runtime,
        )

