from enum import Enum


class RobotsFailureStrategy(str, Enum):
    """Defines the strategy to use when robots.txt cannot be fetched."""

    ALLOW = "allow"
    DENY = "deny"
    RAISE = "raise"