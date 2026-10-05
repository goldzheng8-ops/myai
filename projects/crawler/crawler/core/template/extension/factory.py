
from collections.abc import Callable
from typing import TypeAlias

from core.template.extension.base import TemplateExtension


TemplateExtensionFactory: TypeAlias = Callable[
    [],
    TemplateExtension,
]