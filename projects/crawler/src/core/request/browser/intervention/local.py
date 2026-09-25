from typing import Any

from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.interaction.context import BrowserInteractionContext
from core.request.browser.intervention.base import HumanInterventionEngine


class LocalHumanInterventionEngine(
    HumanInterventionEngine,
):

    async def intervene(
        self,
        context: BrowserInteractionContext[Any],
        inspection: BrowserPageInspection,
    ) -> None:

        response = self._get_response(
            context.request,
        )

        page = response.page

        print()
        print("=" * 60)
        print("Human intervention required.")
        print(f"State: {inspection.state.value}")
        print(f"URL: {inspection.url}")
        print(f"Reason: {inspection.reason}")
        print("=" * 60)
        print()
        print("Please complete the required action")
        print("in the browser window.")
        print()
        print("Press ENTER after completion...")

        await asyncio.to_thread(
            input,
        )

        print("Human intervention completed.")