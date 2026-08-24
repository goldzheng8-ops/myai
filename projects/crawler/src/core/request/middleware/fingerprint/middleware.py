from core.request.context import RequestContext
from core.request.middleware.config import MiddlewareConfig
from core.request.middleware.fingerprint.provider import FingerprintProvider
from core.request.middleware import RequestMiddleware, RequestMiddlewareNext


class FingerprintMiddleware(
    RequestMiddleware,
):
    """
    Calculate and attach the fingerprint of a request.

    The middleware delegates fingerprint calculation to a
    FingerprintProvider.
    """

    def __init__(
        self,
        provider: FingerprintProvider,
        config: MiddlewareConfig | None = None,
    ) -> None:
        super().__init__(
            config
            if config is not None
            else MiddlewareConfig(),
        )
        self._provider =provider

    @property
    def provider(
        self,
    ) -> FingerprintProvider:

        return self._provider

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        if context.fingerprint is None:

            context.fingerprint = (
                self._provider.fingerprint(
                    context.descriptor,
                )
            )

        return await next_(
            context,
        )