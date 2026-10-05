import logging

from core.event.handler import EventHandler
from core.request.events.completed import RequestCompleted


logger = logging.getLogger(__name__)


class RequestCompletedHandler(
    EventHandler[RequestCompleted],
):
    async def handle(
        self,
        event: RequestCompleted,
    ) -> None:

        logger.info(
            "Request completed: %s",
            event.request.url,
        )