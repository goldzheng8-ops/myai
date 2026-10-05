from core.request.context import RequestContext
from core.request.middleware.user_agent.config import StaticUserAgentProviderConfig
from core.request.middleware.user_agent.provider import UserAgentProvider


class StaticUserAgentProvider(
    UserAgentProvider[
        StaticUserAgentProviderConfig
    ],
):
    async def get(
        self,
        context: RequestContext,
    ) -> str:
        return self.config.user_agent