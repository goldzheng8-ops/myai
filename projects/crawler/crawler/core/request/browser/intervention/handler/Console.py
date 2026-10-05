import asyncio
from typing import Any

from core.request.browser.inspector.model import BrowserPageInspection
from core.request.browser.interaction.context import BrowserInteractionContext
from core.request.browser.intervention.handler.base import HumanInterventionHandler


class ConsoleHumanInterventionHandler(
    HumanInterventionHandler,
):

    async def wait_for_intervention(
        self,
        context: BrowserInteractionContext[Any],
        inspection: BrowserPageInspection,
    ) -> None:

        message = self._build_message(
            inspection,
        )

        await asyncio.to_thread(
            input,
            message,
        )

    @staticmethod
    def _build_message(
        inspection: BrowserPageInspection,
    ) -> str:

        reason = (
            inspection.reason
            or "Manual intervention required."
        )

        return (
            "\n"
            "========================================\n"
            "Browser manual intervention required\n"
            "========================================\n"
            f"State : {inspection.state.value}\n"
            f"URL   : {inspection.url}\n"
            f"Title : {inspection.title}\n"
            f"Reason: {reason}\n"
            "\n"
            "Complete the required action in the browser,\n"
            "then press ENTER to continue.\n"
            "========================================\n"
        )