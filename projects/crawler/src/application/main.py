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
        "application.yaml",
    )

    try:
        await application.run()
    finally:
        await application.close()


if __name__ == "__main__":
    asyncio.run(main())