from models.config.value.template import TemplateValueConfig
from models.runtime.extract.context import ExtractContext
from models.enums.value_type import ValueType
from core.template.manager.default import DefaultTemplateManager
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