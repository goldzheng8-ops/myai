
from typing import Any

from application.config import ApplicationConfig
from core.output.engine import OutputEngine
from core.output.factory import DownloadFilenameResolverFactory, OutputSinkFactory, StorageFactory
from core.output.output_resolver import OutputResolver
from core.provider import ProviderBuilder, ProviderResolver
from core.template.manager.base import TemplateManager


def register_outputs(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:

    builder.add_type(StorageFactory)
    builder.add_factory(
        DownloadFilenameResolverFactory,
        lambda resolver: (
            DownloadFilenameResolverFactory(
                template_manager=resolver.resolve(
                    TemplateManager,
                ),
            )
        ),
    )

    builder.add_factory(
        OutputSinkFactory,
        lambda resolver: OutputSinkFactory(
            storage_factory=resolver.resolve(
                StorageFactory,
            ),
            filename_resolver_factory=resolver.resolve(
                DownloadFilenameResolverFactory,
            ),
        ),
    )
    def build_output_resolver_factory(
        resolver: ProviderResolver[Any, Any],
    ) -> Any:

        output_sink_factory:OutputSinkFactory = resolver.resolve(
            OutputSinkFactory,
        )
        sinks = output_sink_factory.create_all(
            config.output_sinks,
        )
        # return an OutputResolver instance constructed with the resolved sinks
        return OutputResolver(sinks)

    builder.add_factory(
        OutputResolver,
        lambda resolver: build_output_resolver_factory(
            resolver
        )
    )

    builder.add_factory(
        OutputEngine,
        lambda resolver: OutputEngine(
            output_resolver=resolver.resolve(
                OutputResolver,
            ),
        ),    
    )