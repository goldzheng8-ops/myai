class RobotsDenied(Exception):
    """Request rejected by robots.txt."""

    def __init__(
        self,
        *,
        url: str,
        user_agent: str,
    ) -> None:
        super().__init__(
            f"Request disallowed by robots.txt: "
            f"url={url!r}, "
            f"user_agent={user_agent!r}",
        )

        self.url = url
        self.user_agent = user_agent

class RobotsFetchError(RuntimeError):
    """Raised when robots.txt cannot be fetched."""
