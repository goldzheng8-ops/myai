from adapters.base import ResponseAdapter

from config.value.template import TemplateValueConfig
from enums.value_type import ValueType
from extractor.value.base import ValuePlugin

from extractor.value.template.renderer.base import TemplateRenderer
from core.context.runtime_context import ObjectContext
from core.context.extract_context import ExtractContext

class TemplateValuePlugin(
    ValuePlugin[TemplateValueConfig],
):

    plugin_type = ValueType.TEMPLATE

    config_type = TemplateValueConfig

    def __init__(
        self,
        renderer: TemplateRenderer,
    ) -> None:

        self._renderer = renderer

    async def extract(
        self,
        *,
        response: ResponseAdapter,
        context: ExtractContext,
        object_context: ObjectContext,
        config: TemplateValueConfig,
    ) -> str:

        return self._renderer.render(
            config.template,
            object_context,
        )