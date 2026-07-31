
from core.template.adapter.base import RenderableTemplate
from core.template.cache.base import TemplateCache



class NullTemplateCache(
    TemplateCache,
):

    def get(
        self,
        key: str,
    ) -> RenderableTemplate | None:

        return None

    def put(
        self,
        key: str,
        template: RenderableTemplate,
    ) -> None:

        pass

    def clear(
        self,
    ) -> None:

        pass