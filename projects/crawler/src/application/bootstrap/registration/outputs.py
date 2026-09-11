
from application.config import ApplicationConfig
from core.output.engine import OutputEngine
from core.output.factory import OutputSinkFactory
from core.output.resolver import OutputResolver
from core.provider import ProviderBuilder


def register_outputs(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:

    sinks = OutputSinkFactory().create_all(
        config.output_sinks,
    )

    resolver = OutputResolver(sinks)

    builder.add_instance(
        OutputResolver,
        resolver,
    )

    builder.add_factory(
        OutputEngine,
        lambda resolver: OutputEngine(
            output_resolver=resolver.resolve(
                OutputResolver,
            ),
        ),    
    )