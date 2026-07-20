from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import ClassVar, Generic, TypeVar


from transform.config.base import TransformConfig
from transform.config.enums import TransformType


InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class TransformPlugin(
    Generic[InputT,OutputT],
    ABC,
):

    type: ClassVar[TransformType]

    @abstractmethod
    def transform_one(
        self,
        value: InputT,
        config: TransformConfig,
    ) -> OutputT:
        ...

    def transform_many(
        self,
        values: Iterable[InputT],
        config: TransformConfig,
    ) -> list[OutputT]:
        return [
            self.transform_one(v, config)
            for v in values
        ]