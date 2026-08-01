from abc import ABC, abstractmethod
from typing import Generic

from .typing import T
from core.plugin.base import Plugin

class BaseMerger(
    Plugin,
    Generic[T],
    ABC,
):


    def merge(
        self,
        parent: T,
        child: T | None,
    ) -> T:

        if child is None:
            return parent

        return self.do_merge(
            parent,
            child,
        )


    @abstractmethod
    def do_merge(
        self,
        parent: T,
        child: T,
    ) -> T:
        ...