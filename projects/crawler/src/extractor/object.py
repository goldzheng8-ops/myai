from typing import Any

from config.extractor.field import FieldConfig
from enums.extract_type import ExtractType
from extractor.base import Extractor
from extractor.exception import MissingFieldError
from extractor.transform.engine import TransformEngine
from extractor.value.engine import ValueEngine
from core.context.extract_context import ExtractContext

class ObjectExtractor(
    Extractor[ObjectConfig],
):
    plugin_type = ExtractType.OBJECT
    config_type = ObjectConfig

    def __init__(
        self,
        executor: ExtractExecutor,
    ) -> None:
        self._executor = executor

    async def extract(
        self,
        config: ObjectConfig,
        context: ExtractContext,
    ) -> dict[str, Any]:

        result: dict[str, Any] = {}

        for child in config.children:

            result[child.name] = (
                await self._executor.extract(
                    child,
                    context,
                )
            )

        return result