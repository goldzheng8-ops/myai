
from extractor.value.template.adapter.base import RenderableTemplate
from extractor.value.template.cache.base import TemplateCache



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