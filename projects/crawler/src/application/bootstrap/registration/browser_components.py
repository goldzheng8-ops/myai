

from application.config.model import ApplicationConfig
from core.provider import ProviderBuilder
from core.request.browser.runtime_manager import BrowserRuntimeManager

def register_browser_components(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:

    builder.add_factory(
        BrowserRuntimeManager,
        lambda resolver: BrowserRuntimeManager(
            config=config.browser_runtime,
            context_config=config.browser_context,

        ),
    )
