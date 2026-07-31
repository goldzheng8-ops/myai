from typing import Iterable

from extractor.template.extension.base import TemplateExtension


class TemplateExtensionRegistry:

    def __init__(self):

        self._extensions: list[
            TemplateExtension
        ] = []

    def register(
        self,
        extension: TemplateExtension,
    ) -> None:

        self._extensions.append(
            extension,
        )

    def extensions(
        self,
    ) -> Iterable[
        TemplateExtension
    ]:

        return tuple(
            self._extensions,
        )