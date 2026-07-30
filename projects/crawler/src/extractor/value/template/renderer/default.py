from __future__ import annotations



from extractor.value.template.manager.base import TemplateManager
from extractor.value.template.renderer.base import TemplateRenderer
from core.context.runtime_context import ObjectContext



class DefaultTemplateRenderer(
    TemplateRenderer,
):

    def __init__(
        self,
        manager: TemplateManager,
    ) -> None:

        self._manager = manager

    def render(
        self,
        template: str,
        context: ObjectContext,
    ) -> str:

        return self._manager.load(
            template,
        ).render(
            context,
        )