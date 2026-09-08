import logging

from core.event.handler import EventHandler
from core.request.events.skipped import RequestSkipped


logger = logging.getLogger(__name__)


class RequestSkippedHandler(
    EventHandler[RequestSkipped],
):
    async def handle(
        self,
        event: RequestSkipped,
    ) -> None:

        logger.warning(
            "Request skipped: url=%s reason=%s",
            event.request.url,
            event.reason,
        )