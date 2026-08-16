from core.request.context import RequestContext
from core.request.middleware.fingerprint.provider import FingerprintProvider,DefaultFingerprintProvider
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
        provider: FingerprintProvider | None = None,
    ) -> None:

        self._provider = (
            provider
            if provider is not None
            else DefaultFingerprintProvider()
        )

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