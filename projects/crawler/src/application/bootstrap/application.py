from application.bootstrap.factory import ApplicationContainerFactory
from application.config import YamlConfigLoader
from application.crawler.application import CrawlerApplication


class ApplicationBootstrap:

    def __init__(
        self,
        config_loader: YamlConfigLoader,
        container_factory: ApplicationContainerFactory,
    ) -> None:

        self._config_loader = config_loader
        self._container_factory = container_factory

    def create(
        self,
        path: str,
    ) -> CrawlerApplication:

        config = self._config_loader.load(
            path,
        )

        container = self._container_factory.create(
            config,
        )

        return container.resolve(
            CrawlerApplication,
        )