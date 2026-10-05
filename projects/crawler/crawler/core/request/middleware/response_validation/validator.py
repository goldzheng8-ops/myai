from abc import ABC, abstractmethod

from core.request.result import RequestResult


class ResponseValidator(ABC):

    @abstractmethod
    def validate(
        self,
        result: RequestResult,
    ) -> None:
        raise NotImplementedError