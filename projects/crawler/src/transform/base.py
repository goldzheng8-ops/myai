from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import ClassVar, Generic, TypeVar

from models.config.transform.base import TransformConfig
from models.enums.transform_type import TransformType
from core.plugin.base import Plugin




InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")
ConfigT=TypeVar("ConfigT", bound=TransformConfig)

class TransformPlugin(
    Plugin,
    Generic[InputT,OutputT,ConfigT],
    ABC,
):

    type: ClassVar[TransformType]

    @abstractmethod
    def transform_one(
        self,
        value: InputT,
        config: ConfigT,
    ) -> OutputT:
        ...

    def transform_many(
        self,
        values: Iterable[InputT],
        config: ConfigT,
    ) -> list[OutputT]:
        return [
            self.transform_one(v, config)
            for v in values
        ]