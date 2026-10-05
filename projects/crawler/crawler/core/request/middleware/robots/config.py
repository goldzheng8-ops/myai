from pydantic import Field

from core.request.middleware.robots.typing import RobotsFailureStrategy
from core.typing.config import BaseConfig
class RobotsPolicyConfig(BaseConfig):
    """
    Runtime configuration of throttling.
    """

    timeout: float = Field(
        default=10.0,
        gt=0,
    )

    ttl: float = Field(
        default=3600.0,
        gt=0,
    )

    failure_strategy: RobotsFailureStrategy = (
        RobotsFailureStrategy.ALLOW
    )

    failure_ttl: float = Field(
        default=60.0,
        gt=0,
    )