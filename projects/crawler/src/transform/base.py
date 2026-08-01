from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import ClassVar, Generic, TypeVar

from models.config.transform.base import TransformConfig
from models.enums.transform_type import TransformType
from core.plugin.base import Plugin




InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class TransformPlugin(
    Plugin,
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