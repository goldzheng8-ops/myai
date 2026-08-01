from models.config.value.selector import SelectorValueConfig
from models.runtime.extract.context import ExtractContext
from core.pipeline.base import  PipelineExecutor
from models.enums.value_type import ValueType
from resolver.base import Resolver


class SelectorResolver(
    Resolver[SelectorValueConfig],
):

    plugin_type = ValueType.SELECTOR


    def __init__(
        self,
        pipeline:PipelineExecutor,
    ):
        self._pipeline = pipeline


    async def resolve(
        self,
        config:SelectorValueConfig,
        context:ExtractContext,
    ):

        selector = config.selector

        if context.response.is_node_selector(selector.type):

            parent = context.node

            if parent is None:

                nodes = await context.response.select_nodes(
                    selector,
                )

            else:

                nodes = await parent.select_nodes(
                    selector,
                )

            return await self._pipeline.execute(
                nodes,
                selector,
            )

        return await context.response.select(
            selector,
        )
