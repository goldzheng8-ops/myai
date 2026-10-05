

from typing import Any

from application.config.model import ApplicationConfig
from core.provider.protocol import ProviderResolver
from core.request.browser.intervention.base import HumanInterventionEngine
from core.request.browser.intervention.handler.Console import ConsoleHumanInterventionHandler
from core.request.browser.intervention.manual import ManualHumanInterventionEngine
from core.request.browser.intervention.registry import HumanInterventionEngineFactory


def build_manual_console_intervention_factory(
    *,
    resolver: ProviderResolver[Any, Any],
    config: ApplicationConfig,
) -> HumanInterventionEngineFactory:

    def factory() -> HumanInterventionEngine:
        return ManualHumanInterventionEngine(
            handler=resolver.resolve(
                ConsoleHumanInterventionHandler,
            ),
            config=config.human_intervention,
        )

    return factory