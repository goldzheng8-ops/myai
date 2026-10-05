from core.extraction.response import ResponseAdapter
from core.request.context import RequestContext
from core.request.discovery.config import PaginationDiscoveryConfig
from core.request.discovery.exception import DiscoveryError
from core.request.discovery.typing import DiscoveryType
from core.request.discovery.url.base import UrlDiscoveryPlugin


class PaginationDiscoveryPlugin(
    UrlDiscoveryPlugin[PaginationDiscoveryConfig],
):

    plugin_type = DiscoveryType.PAGINATION
    config_type = PaginationDiscoveryConfig

    async def urls(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: PaginationDiscoveryConfig,
    ) -> list[str]:

        self._validate_config(config)

        return [
            config.url_template.format(page=page)
            for page in self._page_range(config)
        ]

    @staticmethod
    def _page_range(
        config: PaginationDiscoveryConfig,
    ) -> range:

        stop = (
            config.end_page + 1
            if config.step > 0
            else config.end_page - 1
        )

        return range(
            config.start_page,
            stop,
            config.step,
        )

    @staticmethod
    def _validate_config(
        config: PaginationDiscoveryConfig,
    ) -> None:

        if config.step == 0:
            raise DiscoveryError(
                "Pagination step cannot be zero.",
            )

        if (
            config.step > 0
            and config.start_page > config.end_page
        ):
            raise DiscoveryError(
                "Pagination start_page must not be greater "
                "than end_page when step is positive.",
            )

        if (
            config.step < 0
            and config.start_page < config.end_page
        ):
            raise DiscoveryError(
                "Pagination start_page must not be less "
                "than end_page when step is negative.",
            )