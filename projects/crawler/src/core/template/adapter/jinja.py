# template/adapter/jinja.py

from jinja2 import Template

from core.runtime import RuntimeContext

from .base import RenderableTemplate


class JinjaRenderableTemplate(
    RenderableTemplate,
):

    def __init__(
        self,
        source: str,
        template: Template,
    ) -> None:

        self._source = source
        self._template = template

    @property
    def source(
        self,
    ) -> str:

        return self._source

    def render(
        self,
        context: RuntimeContext,
    ) -> str:

        return self._template.render(
            **context.as_mapping(),
        )