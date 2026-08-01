from .base import BaseMerger
from .typing import T

class ReplaceMerger(
    BaseMerger[T],
):

    plugin_type = "replace"


    def do_merge(
        self,
        parent: T,
        child: T,
    ) -> T:

        return child