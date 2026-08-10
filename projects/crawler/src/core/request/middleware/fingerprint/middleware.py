from core.request.context import RequestContext
from core.request.middleware.fingerprint.provider import FingerprintProvider,DefaultFingerprintProvider
from core.request.middleware import RequestMiddleware, RequestMiddlewareNext


class FingerprintMiddleware(
    RequestMiddleware,
):
    """
    Calculate and attach the fingerprint of a request.

    The middleware itself does not implement the fingerprint
    algorithm. The algorithm is delegated to FingerprintProvider.
    """

    def __init__(
        self,
        provider: FingerprintProvider | None = None,
    ) -> None:

        if provider is None:
            provider = DefaultFingerprintProvider()

        self._provider = provider

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

        context.fingerprint = self._provider.fingerprint(
            context.descriptor,
        )

        return await next_(
            context,
        )