from copy import deepcopy

from .base import BaseMerger
from .typing import T

class ReplaceMerger(
    BaseMerger[T],
):
    """
    Replace parent with child.
    """

    plugin_type = "replace"

    def do_merge(
        self,
        parent: T,
        child: T,
    ) -> T:

        return deepcopy(child)