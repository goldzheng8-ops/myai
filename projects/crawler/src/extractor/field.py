from typing import Any

from models.config.extractor.field import FieldConfig
from models.enums.extract_type import ExtractType
from extractor.base import Extractor
from value.evaluator import ValueExecutor
from models.runtime.extract.context import ExtractContext


class FieldExtractor(
    Extractor[FieldConfig],
):

    plugin_type = ExtractType.FIELD


    def __init__(
        self,
        executor: ValueExecutor,
    ):
        self._executor = executor

    async def extract(
        self,
        config: FieldConfig,
        context: ExtractContext,
    ) -> Any:


        value = await self._executor.resolve(
            config.source,
            context,
            config.transforms,
        )


        if value is None:


            if config.required:

                raise ValueError(
                    f"Required field missing: {config.name}"
                )


            return config.default


        return value