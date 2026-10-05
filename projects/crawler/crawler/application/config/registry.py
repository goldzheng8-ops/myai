from application.config.model import ApplicationConfig
from core.spider.config import SpiderConfigUnion


class SpiderConfigRegistry:

    def __init__(
        self,
        config: ApplicationConfig,
    ) -> None:

        self._configs = {
            spider.name: spider
            for spider in config.spiders
        }

    def get(
        self,
        name: str,
    ) -> SpiderConfigUnion:

        try:
            return self._configs[name]
        except KeyError:
            raise KeyError(
                f"Spider configuration not found: {name!r}"
            ) from None

    def first_name(self) -> str:
        try:
            return next(iter(self._configs))
        except StopIteration as exc:
            raise RuntimeError(
                "No spider configuration is registered."
            ) from exc