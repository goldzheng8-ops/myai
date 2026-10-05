

from core.extraction.selector.selection.base import SelectionStrategy
from core.extraction.selector.selection.factory import SelectionFactory
from core.extraction.selector.selection.mode import SelectionMode
from core.registry.base import Registry


class SelectionRegistry(
    Registry[
        SelectionMode,
        SelectionFactory,
    ],
):
    """
    Registry of selection strategy factories.
    """

    def create(
        self,
        mode: SelectionMode,
    ) -> SelectionStrategy:

        return self.get(mode)()