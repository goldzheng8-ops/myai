import logging

from core.event.handler import EventHandler
from core.request.events.started import RequestStarted


logger = logging.getLogger(__name__)


class RequestStartedHandler(
    EventHandler[RequestStarted],
):
    async def handle(
        self,
        event: RequestStarted,
    ) -> None:

        logger.info(
            "Request started: %s",
            event.request.url,
        )