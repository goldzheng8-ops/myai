import asyncio

from core.request.browser.runtime_manager import BrowserRuntimeDebugger
from core.request.browser.snapshot import BrowserPageRuntimeState, BrowserPageSnapshot, BrowserPageSnapshotBuilder
from core.request.browser.stabilizer.base import BrowserPageStabilizer
from core.request.browser.stabilizer.policy.registry import BrowserPageStabilityPolicyRegistry
from core.request.browser.typing import BrowserInteractionPhase
from playwright.async_api import Page



class PlaywrightBrowserPageStabilizer(
    BrowserPageStabilizer,
):

    def __init__(
        self,
        snapshot_builder: BrowserPageSnapshotBuilder,
        policy_registry: BrowserPageStabilityPolicyRegistry,
        debugger: BrowserRuntimeDebugger,
    ) -> None:

        self._snapshot_builder = snapshot_builder
        self._policies = policy_registry
        self._debugger = debugger

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

        debugger = self._debugger

        debugger.log_snapshot(
            phase=phase,
            snapshot=previous,
        )

        for attempt in range(
            policy.max_attempts,
        ):
            await asyncio.sleep(
                policy.interval,
            )

            current = await self._snapshot_builder.build(
                page,
                runtime_state,
            )

            stable = policy.is_stable(
                previous,
                current,
            )

            debugger.log_snapshot(
                phase=phase,
                attempt=attempt + 1,
                stable=stable,
                snapshot=current,
            )

            if stable:

                # debugger.log_stable_page(
                #     snapshot=current,
                # )

                await debugger.log_page_environment(
                    page=page,
                )
                return current

            previous = current


        debugger.log_stabilizer_timeout(
            phase=phase,
            snapshot=previous,
        )

        return previous