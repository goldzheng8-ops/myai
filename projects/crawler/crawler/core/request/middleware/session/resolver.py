from abc import ABC, abstractmethod

from core.request.descriptor import RequestDescriptor


class SessionIdResolver(ABC):

    @abstractmethod
    def resolve(
        self,
        descriptor: RequestDescriptor,
    ) -> str | None:
        raise NotImplementedError


class DefaultSessionIdResolver(
    SessionIdResolver,
):

    def __init__(
        self,
        default_session_id: str | None = None,
    ) -> None:
        self._default_session_id = default_session_id

    @property
    def default_session_id(
        self,
    ) -> str | None:
        return self._default_session_id

    def resolve(
        self,
        descriptor: RequestDescriptor,
    ) -> str | None:
        return self._default_session_id