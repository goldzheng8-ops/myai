from abc import ABC, abstractmethod
from typing import Generic, TypeVar



from .base import ResponseAdapter
from core.request.response import (
    BrowserResponse,
    RequestResponse,
)

from .adapter import (
    BrowserResponseAdapter,
    StaticResponseAdapter,
)


SourceT = TypeVar("SourceT")
AdapterT = TypeVar("AdapterT")


class AdapterFactory(
    Generic[SourceT, AdapterT],
    ABC,
):
    """
    Factory for converting a source object
    into a normalized adapter.
    """

    @abstractmethod
    def create(
        self,
        source: SourceT,
    ) -> AdapterT:
        raise NotImplementedError



class ResponseAdapterFactory(
    AdapterFactory[
        RequestResponse,
        ResponseAdapter,
    ],
):
    """
    Factory for converting transport responses
    into extraction-layer response adapters.
    """

    @abstractmethod
    def create(
        self,
        source: RequestResponse,
    ) -> ResponseAdapter:
        raise NotImplementedError

class DefaultResponseAdapterFactory(
    ResponseAdapterFactory,
):
    """
    Default response adapter factory.

    Selects an adapter according to the
    transport response source.
    """

    def create(
        self,
        source: RequestResponse,
    ) -> ResponseAdapter:

        if isinstance(source, BrowserResponse):
            return BrowserResponseAdapter(
                source,
            )

        return StaticResponseAdapter(
            source,
        )