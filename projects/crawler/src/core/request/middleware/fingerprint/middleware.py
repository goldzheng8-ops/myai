from core.request.context import RequestContext
from core.request.middleware.config import FingerprintMiddlewareConfig
from core.request.middleware.fingerprint.provider import FingerprintProvider
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.typing import MiddlewareType, RequestMiddlewareNext

class FingerprintMiddleware(
    RequestMiddleware[FingerprintMiddlewareConfig],
):
    """
    Calculate and attach the fingerprint of a request.

    The middleware delegates fingerprint calculation to a
    FingerprintProvider.
    """
    plugin_type = MiddlewareType.FINGERPRINT
    def __init__(
        self,
        provider: FingerprintProvider,
        config: FingerprintMiddlewareConfig,
    ) -> None:
        super().__init__(
            config
        )
        self._provider =provider

    @property
    def provider(
        self,
    ) -> FingerprintProvider:

        return self._provider
    @property
    def config(self) -> FingerprintMiddlewareConfig:
        return self._config
    
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