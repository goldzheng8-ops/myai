from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from core.plugin import Plugin
from .typing import MiddlewareType, RequestMiddlewareNext
from ..context import RequestContext

class MiddlewarePlugin(
    Plugin,
    ABC,
):
    """
    Public contract implemented by all request downloaders.
    """

    type: ClassVar[MiddlewareType]

    @abstractmethod
    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:
        """
        Process a request context.

        Implementations may perform work before calling
        next_, after calling next_, or both.
        """

        raise NotImplementedError