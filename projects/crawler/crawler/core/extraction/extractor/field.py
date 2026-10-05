from core.extraction.exception import RequiredFieldMissingError
from core.extraction.extractor.base import Extractor
from core.extraction.extractor.config import FieldConfig
from core.extraction.extractor.result import ExtractResult
from core.extraction.extractor.typing import ExtractType
from core.extraction.value.evaluator import ValueExecutor
from core.extraction.extractor.context import ExtractContext


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
    ) -> ExtractResult:


        value = await self._executor.resolve(
            config.source,
            context,
            config.transforms,
        )


        if value is None:


            if config.required:

                raise RequiredFieldMissingError(
                    f"Required field missing: {config.name}"
                )


            return ExtractResult(
                data=config.default,
            )

        return ExtractResult(
            data=value,
            metadata=config.metadata.copy(),
        )