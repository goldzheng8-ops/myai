from config.value.selector import SelectorValueConfig
from core.context.extract_context import ExtractContext
from core.pipeline.base import Pipeline
from enums.value_type import ValueType
from resolver.base import Resolver


class SelectorResolver(
    Resolver[SelectorValueConfig],
):

    plugin_type = ValueType.SELECTOR


    def __init__(
        self,
        pipeline:Pipeline,
    ):
        self._pipeline = pipeline


    async def resolve(
        self,
        config:SelectorValueConfig,
        context:ExtractContext,
    ):

        node = context.node

        if node is None:
            nodes = await context.response.select_nodes(
                config.selector,
            )

        else:
            nodes = await node.select_nodes(
                config.selector,
            )


        return await self._pipeline.execute(
            nodes,
            config.selector,
        )