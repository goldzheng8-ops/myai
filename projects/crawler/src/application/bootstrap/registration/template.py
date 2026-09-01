
from core.provider import ProviderBuilder
from core.template.cache.base import TemplateCache
from core.template.cache.memory import MemoryTemplateCache
from core.template.backend.base import TemplateBackend
from core.template.backend.jinja import JinjaBackend
from core.template.manager.default import DefaultTemplateManager
from core.template.backend.config import JinjaTemplateConfig
from core.template.extension.manager import TemplateExtensionManager, TemplateExtensionRegistry

import pkgutil
import importlib
import inspect

from core.template.extension.base import TemplateExtension

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
    # discover and register extensions from known template packages
    packages = [
        "core.template.filters",
        "core.template.globals",
        "core.template.tests",
    ]

    for pkg_name in packages:
        try:
            pkg = importlib.import_module(pkg_name)
        except Exception:
            continue

        # only packages have __path__ to iterate submodules
        if not hasattr(pkg, "__path__"):
            continue

        for _, modname, _ in pkgutil.iter_modules(pkg.__path__):
            full_name = f"{pkg_name}.{modname}"
            try:
                mod = importlib.import_module(full_name)
            except Exception:
                continue

            for _, obj in inspect.getmembers(mod, inspect.isclass):
                # ensure class is defined in this module
                if getattr(obj, "__module__", None) != full_name:
                    continue

                try:
                    if issubclass(obj, TemplateExtension) and obj is not TemplateExtension:
                        registry.register((obj.plugin_type, obj.name), obj)
                except Exception:
                    # skip non-concrete or malformed classes
                    continue

    return registry