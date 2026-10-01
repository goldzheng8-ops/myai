from abc import ABC, abstractmethod

from core.request.middleware.auth.auth_provider.oauth2.models import OAuth2TokenSet


class OAuth2TokenStore(ABC):

    @abstractmethod
    async def get(
        self,
        key: str,
    ) -> OAuth2TokenSet | None:
        raise NotImplementedError

    @abstractmethod
    async def set(
        self,
        key: str,
        token_set: OAuth2TokenSet,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(
        self,
        key: str,
    ) -> None:
        raise NotImplementedError

class InMemoryOAuth2TokenStore(
    OAuth2TokenStore,
):

    def __init__(self) -> None:
        self._tokens: dict[str, OAuth2TokenSet] = {}

    async def get(
        self,
        key: str,
    ) -> OAuth2TokenSet | None:
        return self._tokens.get(key)

    async def set(
        self,
        key: str,
        token_set: OAuth2TokenSet,
    ) -> None:
        self._tokens[key] = token_set

    async def remove(
        self,
        key: str,
    ) -> None:
        self._tokens.pop(key, None)