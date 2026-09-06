from __future__ import annotations

from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import RobotMiddlewareConfig
from core.request.middleware.robot.policy import RobotsPolicy
from core.request.middleware.typing import MiddlewareType, RequestMiddlewareNext
from core.request.middleware.robot.exceptions import RobotsDenied

        
class RobotMiddleware(
    RequestMiddleware[
        RobotMiddlewareConfig,
    ],
):

    plugin_type = MiddlewareType.ROBOT

    def __init__(
        self,
        policy: RobotsPolicy,
        config: RobotMiddlewareConfig,
    ) -> None:
        super().__init__(config)
        self._policy = policy

    @property
    def policy(self) -> RobotsPolicy:
        return self._policy

    @property
    def config(self) -> RobotMiddlewareConfig:
        return self._config

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        user_agent = self._resolve_user_agent(
            context,
        )

        allowed = await self._policy.allowed(
            url=context.descriptor.url,
            user_agent=user_agent,
        )

        if not allowed:
            raise RobotsDenied(
                url=context.descriptor.url,
                user_agent=user_agent,
            )

        return await next_(context)

    def _resolve_user_agent(
        self,
        context: RequestContext,
    ) -> str:

        if self.config.user_agent is not None:
            return self.config.user_agent

        for name, value in (
            context.descriptor.headers.items()
        ):
            if name.lower() == "user-agent":
                return value

        return "*"