from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from jinja2 import Environment
from jinja2 import StrictUndefined
from jinja2 import Template

from extractor.value.utils.object_context import ObjectContext

def filter_strip(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    return value


def filter_lower(value: Any) -> Any:
    if isinstance(value, str):
        return value.lower()
    return value


def filter_upper(value: Any) -> Any:
    if isinstance(value, str):
        return value.upper()
    return value

class TemplateRenderer(ABC):

    @abstractmethod
    def render(
        self,
        template: str,
        context: ObjectContext,
    ) -> str:
        ...

class DefaultTemplateRenderer(TemplateRenderer):

    def render(
        self,
        template: str,
        context: ObjectContext,
    ) -> str:

        return template.format_map(context.as_mapping())
class JinjaTemplateRenderer(
    TemplateRenderer,
):

    def __init__(
        self,
        *,
        undefined=StrictUndefined,
        autoescape: bool = False,
    ) -> None:
        self._cache: dict[
            str,
            Template,
        ] = {}
        self._environment = Environment(
            autoescape=autoescape,
            undefined=undefined,
            enable_async=False,
        )
        self._register_filters()
        self._register_globals()
        self._register_tests()

    def render(
        self,
        template: str,
        context: ObjectContext,
    ) -> str:

        return self._compile(
            template,
        ).render(
            **context.as_mapping(),
        )

    def _register_filters(
        self,
    ) -> None:
        filters = self._environment.filters

        filters["strip"] = filter_strip
        filters["lower"] = filter_lower
        filters["upper"] = filter_upper

    def _register_globals(
        self,
    ) -> None:

        self._environment.globals["len"] = len

        self._environment.globals["max"] = max

        self._environment.globals["min"] = min

    def _register_tests(
        self,
    ) -> None:

        self._environment.tests["blank"] = lambda s: s == ""

    def _compile(
        self,
        template: str,
    ) -> Template:

        compiled = self._cache.get(template)

        if compiled is None:

            compiled = self._environment.from_string(
                template,
            )

            self._cache[template] = compiled

        return compiled


