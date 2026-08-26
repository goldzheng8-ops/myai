
from core.provider import ProviderBuilder
from core.template.cache.base import TemplateCache
from core.template.cache.memory import MemoryTemplateCache
from core.template.backend.base import TemplateBackend
from core.template.backend.jinja import JinjaBackend
from core.template.manager.default import DefaultTemplateManager
from models.config.template.jinja import JinjaTemplateConfig
from core.template.extension.manager import TemplateExtensionManager, TemplateExtensionRegistry


def register_template(
    builder: ProviderBuilder,
) -> None:
    
    builder.add_type(JinjaTemplateConfig)
    
    builder.add_factory(
        TemplateExtensionRegistry,
        lambda _: create_template_extension_registry(),
    )

    builder.add_factory(
        TemplateExtensionManager,
        lambda resolver: TemplateExtensionManager(
            resolver.resolve(
                TemplateExtensionRegistry,
            ),
        ),
    )

    builder.add_factory(
        TemplateBackend,
        lambda resolver: JinjaBackend(
            config=resolver.resolve(
                JinjaTemplateConfig,
            ),
            extensions=resolver.resolve(
                TemplateExtensionManager,
            ),
        ),
    )

    builder.add_type(
        TemplateCache,
        MemoryTemplateCache,
    )

    builder.add_factory(
        DefaultTemplateManager,
        lambda resolver: DefaultTemplateManager(
            backend=resolver.resolve(
                TemplateBackend,
            ),
            cache=resolver.resolve(
                TemplateCache,
            ),
        ),
    )

def create_template_extension_registry(
) -> TemplateExtensionRegistry:

    registry = TemplateExtensionRegistry()

    registry.register(
        UpperFilterExtension.name,
        UpperFilterExtension(),
    )

    registry.register(
        StripFilterExtension.name,
        StripFilterExtension(),
    )

    registry.register(
        LenGlobalExtension.name,
        LenGlobalExtension(),
    )

    return registry