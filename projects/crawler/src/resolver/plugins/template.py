from config.value.template import TemplateValueConfig
from core.context.extract_context import ExtractContext
from enums.value_type import ValueType
from extractor.value.template.manager.default import DefaultTemplateManager
from resolver.base import Resolver

class TemplateValueResolver(
    Resolver[TemplateValueConfig],
):

    plugin_type = ValueType.TEMPLATE


    def __init__(
        self,
        manager:DefaultTemplateManager,
    ):
        self._manager = manager


    async def resolve(
        self,
        config:TemplateValueConfig,
        context:ExtractContext,
    ):

        return self._manager.render(
            config.template,
            context.runtime,
        )