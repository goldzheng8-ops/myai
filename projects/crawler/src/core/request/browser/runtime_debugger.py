from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.model import BrowserInteractionExecution
from core.request.browser.typing import BrowserInteractionPhase, BrowserPageState
from core.request.browser.interaction.model import BrowserAction
from playwright.async_api import Page, Response
import logging

from core.request.browser.config import BrowserRuntimeConfig
from core.request.browser.snapshot import BrowserPageRuntimeState, BrowserPageSnapshot

logger=logging.getLogger(__name__)

class BrowserRuntimeDebugger:

    def __init__(
        self,
        config: BrowserRuntimeConfig,
    ) -> None:
        self._config = config

    @property
    def config(self) -> BrowserRuntimeConfig:
        return self._config

    # =========================================================
    # Interaction-level logging
    # =========================================================

    def log_action(
        self,
        *,
        index: int,
        action: BrowserAction,
        completed: bool = False,
    ) -> None:

        if completed:
            logger.info(
                "[BrowserAction] "
                "#%d completed",
                index,
            )
            return

        logger.info(
            "[BrowserAction] "
            "#%d type=%s",
            index,
            action.type,
        )

    def log_phase(
        self,
        *,
        previous: BrowserInteractionPhase,
        current: BrowserInteractionPhase,
    ) -> None:

        if previous == current:
            return

        logger.info(
            "[BrowserInteractionPhase] "
            "%s -> %s",
            previous.value,
            current.value,
        )

    def log_intervention(
        self,
        *,
        engine: object,
        state: BrowserPageState,
    ) -> None:

        logger.info(
            "[BrowserIntervention] "
            "engine=%s state=%s",
            type(engine).__name__,
            state.value,
        )

    def log_recovery(
        self,
        *,
        recovered: bool,
    ) -> None:

        if recovered:
            logger.info(
                "[BrowserRecovery] "
                "page recovered.",
            )
            return

        logger.warning(
            "[BrowserRecovery] "
            "page recovery failed.",
        )

    def log_interaction_failed(
        self,
        *,
        phase: BrowserInteractionPhase,
        exc: BaseException,
    ) -> None:

        logger.error(
            "[BrowserInteraction] failed "
            "phase=%s "
            "error=%s",
            phase.value,
            exc,
            exc_info=(
                type(exc),
                exc,
                exc.__traceback__,
            ),
        )

    def log_transitions(
        self,
        execution: BrowserInteractionExecution,
    ) -> None:
        logger.info(
            "[BrowserInteraction] completed "
            "transitions=%s",
            self._format_transitions(
                execution,
            ),
        )               
    # =========================================================
    # Runtime diagnostic logging
    # =========================================================

    def log_snapshot(
        self,
        *,
        snapshot: BrowserPageSnapshot,
        phase: BrowserInteractionPhase,
        stable: bool | None = None,
        attempt: int | None = None,
    ) -> None:

        if attempt is None:
            logger.info(
                "[BrowserSnapshot] "
                "phase=%s %s",
                phase.value,
                self._format_snapshot(snapshot),
            )
            return

        logger.info(
            "[BrowserSnapshot] "
            "attempt=%d "
            "phase=%s "
            "stable=%s "
            "%s",
            attempt,
            phase.value,
            stable,
            self._format_snapshot(snapshot),
        )

    def log_stabilizer_timeout(
        self,
        *,
        phase: BrowserInteractionPhase,
        snapshot: BrowserPageSnapshot,
    ) -> None:

        logger.warning(
            "[BrowserStabilizer] "
            "stability timeout "
            "phase=%s "
            "%s",
            phase.value,
            self._format_snapshot(snapshot),
        )

    def log_detector(
        self,
        *,
        phase: BrowserInteractionPhase,
        snapshot: BrowserPageSnapshot,
        inspection: BrowserPageInspection | None,
    ) -> None:

        if inspection is None:
            logger.info(
                "[BrowserDetector] "
                "phase=%s "
                "state=%s "
                "reason=%r "
                "url=%r",
                phase.value,
                None,
                "no hit any detector",
                snapshot.url,
            )
            return

        logger.info(
            "[BrowserDetector] "
            "phase=%s "
            "state=%s "
            "reason=%r "
            "url=%r",
            phase.value,
            inspection.state.value,
            inspection.reason,
            inspection.url,
        )


    @staticmethod
    def _format_snapshot(
        snapshot: BrowserPageSnapshot,
    ) -> str:

        return (
            f"url={snapshot.url!r} "
            f"title={snapshot.title!r} "
            f"status={snapshot.status_code!r} "
            f"content_type={snapshot.content_type!r} "
            f"body={len(snapshot.body_text)} "
            f"forms={snapshot.has_forms} "
            f"inputs={snapshot.has_inputs} "
            f"iframes={snapshot.has_iframes}"
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
    
    @staticmethod
    def log_stable_page(
        snapshot: BrowserPageSnapshot,
    ) -> None:
        logger.info(
            "[BrowserStabilizer] "
            "stable page body:\n%s",
            snapshot.body_text,
        )

        if snapshot.html is not None:
            logger.debug(
                "[BrowserStabilizer] "
                "stable page html:\n%s",
                snapshot.html,
            )

    async def log_document_response(
        self,
        *,
        state: BrowserPageRuntimeState,
        response: Response,
    ) -> None:

        request = response.request

        logger.info(
            "[BrowserPageResponse] "
            "navigation=%d "
            "resource=%s "
            "method=%s "
            "url=%r "
            "status=%d "
            "content_type=%r",
            state.navigation_count,
            request.resource_type,
            request.method,
            response.url,
            response.status,
            response.headers.get(
                "content-type",
            ),
        )

        logger.info(
            "[BrowserEnvironment] "
            "headless=%s",
            self.config.headless,
        )

        try:
            headers = await request.all_headers()
        except Exception as exc:
            logger.debug(
                "[BrowserDocumentRequest] "
                "failed to read headers: %s",
                exc,
            )
            return

        logger.info(
            "[BrowserDocumentRequest] "
            "method=%s "
            "url=%r "
            "headers=%r",
            request.method,
            request.url,
            headers,
        )

    async def log_page_environment(
        self,
        *,
        page: Page,
    ) -> None:

        try:
            environment = await page.evaluate(
                """
                () => ({
                    userAgent: navigator.userAgent,
                    webdriver: navigator.webdriver,
                    href: location.href,
                    title: document.title,
                })
                """
            )

        except Exception as exc:
            logger.debug(
                "[BrowserEnvironment] "
                "failed to inspect page environment: %s",
                exc,
            )
            return

        logger.info(
            "[BrowserEnvironment] "
            "headless=%s "
            "user_agent=%r "
            "navigator.webdriver=%r "
            "href=%r "
            "title=%r",
            self.config.headless,
            environment["userAgent"],
            environment["webdriver"],
            environment["href"],
            environment["title"],
        )
