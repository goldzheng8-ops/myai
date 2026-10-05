from abc import ABC, abstractmethod

from core.request.middleware.auth.auth_provider.oauth2.models import OAuth2TokenSet
from core.request.middleware.auth.auth_provider.oauth2.typing import OAuth2TokenState
from core.request.middleware.auth.auth_provider.oauth2.models import OAuth2TokenRecord

class OAuth2TokenStore(ABC):

    @abstractmethod
    async def get(
        self,
        *,
        session_id: str,
        key: str,
    ) -> OAuth2TokenRecord | None:
        raise NotImplementedError

    @abstractmethod
    async def set(
        self,
        *,
        session_id: str,
        key: str,
        token_set: OAuth2TokenSet,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def invalidate(
        self,
        *,
        session_id: str,
        key: str,
        reason: str | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(
        self,
        *,
        session_id: str,
        key: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear_session(
        self,
        session_id: str,
    ) -> None:
        raise NotImplementedError

class InMemoryOAuth2TokenStore(OAuth2TokenStore):

    def __init__(self) -> None:
        self._records: dict[
            tuple[str, str],
            OAuth2TokenRecord,
        ] = {}

    async def get(
        self,
        *,
        session_id: str,
        key: str,
    ) -> OAuth2TokenRecord | None:

        return self._records.get(
            (session_id, key),
        )

    async def set(
        self,
        *,
        session_id: str,
        key: str,
        token_set: OAuth2TokenSet,
    ) -> None:

        self._records[
            (session_id, key)
        ] = OAuth2TokenRecord(
            token_set=token_set,
            state=OAuth2TokenState.ACTIVE,
            invalid_reason=None,
        )

    async def invalidate(
        self,
        *,
        session_id: str,
        key: str,
        reason: str | None = None,
    ) -> None:

        self._records[
            (session_id, key)
        ] = OAuth2TokenRecord(
            token_set=None,
            state=OAuth2TokenState.INVALID,
            invalid_reason=reason,
        )

    async def remove(
        self,
        *,
        session_id: str,
        key: str,
    ) -> None:

        self._records.pop(
            (session_id, key),
            None,
        )

    async def clear_session(
        self,
        session_id: str,
    ) -> None:

        keys = tuple(
            key
            for key_session, key in self._records
            if key_session == session_id
        )

        for key in keys:
            self._records.pop(
                (session_id, key),
                None,
            )