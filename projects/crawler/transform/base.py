from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from typing import Any

from transform.config.base import TransformConfig
from transform.config.enums import TransformType

T = TypeVar("T", bound=TransformConfig)

class TransformPlugin(Generic[T],ABC):

    @property
    @abstractmethod
    def type(self)-> TransformType:
        ...

    def transform(self, value: Any, config:T) -> Any:

        if isinstance(value, list):
            return [
                self.transform_one(v, config)
                for v in value
            ]

        return self.transform_one(value, config)

    @abstractmethod
    def transform_one(self, value: Any, config: T) -> Any:
        ...