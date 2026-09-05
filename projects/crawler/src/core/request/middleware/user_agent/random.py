import random
from core.request.context import RequestContext
from core.request.middleware.user_agent.config import RandomUserAgentProviderConfig
from core.request.middleware.user_agent.provider import UserAgentProvider

class RandomUserAgentProvider(
    UserAgentProvider[
        RandomUserAgentProviderConfig
    ],
):
    async def get(
        self,
        context: RequestContext,
    ) -> str | None:

        if not self.config.values:
            return None

        return random.choice(
            self.config.values,
        )