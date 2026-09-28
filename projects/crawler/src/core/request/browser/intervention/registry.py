

from typing import Callable

from core.registry import Registry
from core.request.browser.intervention.base import HumanInterventionEngine
from core.request.browser.typing import BrowserPageState


HumanInterventionEngineFactory = Callable[
    [],
    HumanInterventionEngine,
]

class HumanInterventionEngineRegistry(
    Registry[
        BrowserPageState,
        HumanInterventionEngineFactory,
    ],
):
    """
    Registry of human intervention engine factories.

    Each browser page state may optionally provide an
    intervention strategy.

    Absence of a registered engine means that the state
    does not require human intervention.
    """

    def resolve(
        self,
        state: BrowserPageState,
    ) -> HumanInterventionEngine | None:

        factory = self.get_optional(
            state,
        )

        if factory is None:
            return None

        return factory()