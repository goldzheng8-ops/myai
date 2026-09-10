import asyncio
import logging

from application.bootstrap.application import ApplicationBootstrap
from application.bootstrap.factory import ApplicationContainerFactory
from application.config.loader import YamlConfigLoader


async def main() -> None:
    # Ensure warnings are visible on the console
    logging.basicConfig(level=logging.WARNING)

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