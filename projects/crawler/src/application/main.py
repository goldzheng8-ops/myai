import asyncio

from application.bootstrap.application import ApplicationBootstrap
from application.bootstrap.factory import ApplicationContainerFactory
from application.config.loader import YamlConfigLoader


async def main() -> None:

    bootstrap = ApplicationBootstrap(
        config_loader=YamlConfigLoader(),
        container_factory=ApplicationContainerFactory(),
    )

    application = bootstrap.create(
        "config.yaml",
    )

    await application.run()


if __name__ == "__main__":
    asyncio.run(main())