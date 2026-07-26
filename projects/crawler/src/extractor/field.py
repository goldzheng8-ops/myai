from typing import Any

from extractor.config import FieldConfig
from request.context import RequestContext
from response.adapter import ResponseAdapter
from selector.engine import SelectorEngine
from transform.engine import TransformEngine


class FieldExtractor:

    def __init__(

        self,

        value_engine,

        transform_engine,

    ):

        self._value_engine = value_engine

        self._transform_engine = transform_engine

    async def extract(...):

        value = await self._value_engine.extract(

            response=response,

            context=context,

            config=config.source,

        )

        return await self._transform_engine.transform(

            value=value,

            configs=config.transforms,

        )