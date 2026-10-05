from abc import abstractmethod
from collections.abc import Iterable
from typing import ClassVar, Generic

from core.extraction.transform.context import TransformContext
from core.extraction.transform.typing import TransformType
from core.plugin.base import Plugin
from core.extraction.transform.typing import InputT,OutputT,ConfigT

class TransformPlugin(
    Plugin,
    Generic[InputT, OutputT, ConfigT],
):
    plugin_type: ClassVar[TransformType]

    @abstractmethod
    def transform_one(
        self,
        value: InputT,
        config: ConfigT,
        context: TransformContext | None = None,
    ) -> OutputT:
        ...

    def transform_many(
        self,
        values: Iterable[InputT],
        config: ConfigT,
        context: TransformContext | None = None,
    ) -> list[OutputT]:
        return [
            self.transform_one(
                value,
                config,
                context,
            )
            for value in values
        ]