from urllib.parse import urljoin

from core.extraction.transform.config import UrlResolveTransformConfig
from core.extraction.transform.base import TransformPlugin
from core.extraction.transform.context import TransformContext
from core.extraction.transform.exception import TransformError
from core.extraction.transform.typing import TransformType

class UrlResolveTransform(
    TransformPlugin[
        str,
        str,
        UrlResolveTransformConfig,
    ],
):
    plugin_type = TransformType.URL_RESOLVE

    def transform_one(
        self,
        value: str,
        config: UrlResolveTransformConfig,
        context: TransformContext | None = None,
    ) -> str:

        if context is None:
            raise TransformError(
                "UrlResolveTransform requires "
                "a TransformContext.",
            )

        base_url = context.descriptor.url

        return urljoin(
            base_url,
            value,
        )