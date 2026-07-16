from abc import ABC, abstractmethod


class ResponseAdapter(ABC):

    @abstractmethod
    def xpath(self, query: str, many: bool = False):
        ...

    @abstractmethod
    def css(self, query: str, many: bool = False):
        ...

    @abstractmethod
    def regex(self, pattern: str, many: bool = False):
        ...