from fake_useragent import UserAgent

from core.request.context import RequestContext
from core.request.middleware.user_agent.config import FakeUserAgentProviderConfig
from core.request.middleware.user_agent.provider import UserAgentProvider

class FakeUserAgentProvider(
    UserAgentProvider[
        FakeUserAgentProviderConfig
    ],
):
    def __init__(
        self,
        config: FakeUserAgentProviderConfig,
    ) -> None:

        super().__init__(config)

        self._user_agent = UserAgent()

    async def get(
        self,
        context: RequestContext,
    ) -> str | None:

        return self._user_agent.random