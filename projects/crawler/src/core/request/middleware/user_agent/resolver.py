from typing import Any, Mapping

from core.request.middleware.user_agent.provider import UserAgentProvider


class UserAgentProviderResolver:

    def __init__(
        self,
        providers: Mapping[
            str,
            UserAgentProvider[Any],
        ],
    ) -> None:
        self._providers = providers

    def resolve(
        self,
        name: str,
    ) -> UserAgentProvider[Any]:

        try:
            return self._providers[name]
        except KeyError as exc:
            raise LookupError(
                f"Proxy provider not found: {name!r}",
            ) from exc