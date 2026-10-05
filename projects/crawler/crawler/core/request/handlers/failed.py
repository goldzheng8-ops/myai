import logging

from core.event.handler import EventHandler
from core.request.events.failed import RequestFailed


logger = logging.getLogger(__name__)


class RequestFailedHandler(
    EventHandler[RequestFailed],
):
    async def handle(
        self,
        event: RequestFailed,
    ) -> None:

        logger.error(
            "Request failed: %s",
            event.request.url,
            exc_info=(
                type(event.error),
                event.error,
                event.error.__traceback__,
            ),
        )