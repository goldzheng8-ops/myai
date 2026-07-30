from typing import Any

from config.extractor.field import FieldConfig
from enums.extract_type import ExtractType
from extractor.base import Extractor
from extractor.exception import MissingFieldError
from extractor.transform.engine import TransformEngine
from extractor.value.engine import ValueEngine
from core.context.extract_context import ExtractContext


class FieldExtractor(
    Extractor[FieldConfig],
):

    plugin_type = ExtractType.FIELD

    def __init__(
        self,
        value_engine: ValueEngine,
        transform_engine: TransformEngine,
        selection_dispatch: SelectionDispatchTable,
        extraction_dispatch: ExtractionDispatchTable,
    ) -> None:

        self._value_engine = value_engine

        self._transform_engine = transform_engine

        self._selection_dispatch = selection_dispatch

        self._extraction_dispatch = extraction_dispatch

    async def extract(
        self,
        config: FieldConfig,
        context: ExtractContext,
        executor: ExtractExecutor,
    ) -> ExtractResult:
        source = await self._value_engine.resolve(
            config.source,
            context.runtime,
        )
        if isinstance(
            source,
            SelectorConfig,
        ):
            vars
            