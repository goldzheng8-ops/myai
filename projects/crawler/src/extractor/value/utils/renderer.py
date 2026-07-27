from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

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
