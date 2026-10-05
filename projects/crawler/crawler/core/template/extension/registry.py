from core.registry import Registry
from core.template.extension.base import TemplateExtension
from core.template.extension.factory import TemplateExtensionFactory
from core.template.typing import TemplateExtensionKey


class TemplateExtensionRegistry(
    Registry[
        TemplateExtensionKey,
        TemplateExtensionFactory,
    ],
):
    """
    Registry of template extension factories.
    """

    def create(
        self,
        key:TemplateExtensionKey
    ) -> TemplateExtension:

        return self.get(key)()

