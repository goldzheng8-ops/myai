import asyncio
import logging

from core.request.browser.snapshot import BrowserPageRuntimeState, BrowserPageSnapshot, BrowserPageSnapshotBuilder
from core.request.browser.stabilizer.base import BrowserPageStabilizer
from core.request.browser.stabilizer.policy.registry import BrowserPageStabilityPolicyRegistry
from core.request.browser.typing import BrowserInteractionPhase
from playwright.async_api import Page


logger = logging.getLogger(__name__)


class PlaywrightBrowserPageStabilizer(
    BrowserPageStabilizer,
):

    def __init__(
        self,
        snapshot_builder: BrowserPageSnapshotBuilder,
        policy_registry: BrowserPageStabilityPolicyRegistry,
    ) -> None:
        self._snapshot_builder = snapshot_builder
        self._policies = policy_registry

    async def stabilize(
        self,
        page: Page,
        phase: BrowserInteractionPhase,
        runtime_state: BrowserPageRuntimeState,
    ) -> BrowserPageSnapshot:

        policy = self._policies.resolve(
            phase,
        )

        previous = await self._snapshot_builder.build(
            page,
            runtime_state,
        )

        logger.info(
            "[BrowserStabilizer] initial snapshot "
            "state=%s url=%r title=%r",
            phase,
            previous.url,
            previous.title,
        )

        for attempt in range(
            policy.max_attempts
        ):
            await asyncio.sleep(
                policy.interval,
            )

            current = (
                await self._snapshot_builder.build(
                    page,
                    runtime_state,
                )
            )

            stable = policy.is_stable(
                previous,
                current,
            )

            logger.info(
                "[BrowserStabilizer] "
                "attempt=%d state=%s stable=%s "
                "url=%r title=%r",
                attempt + 1,
                phase,
                stable,
                current.url,
                current.title,
            )

            if stable:
                return current

            previous = current

        logger.info(
            "[BrowserStabilizer] "
            "stability timeout state=%s "
            "url=%r title=%r",
            phase,
            previous.url,
            previous.title,
        )

        return previous