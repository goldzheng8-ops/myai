from copy import deepcopy
from .typing import T
from .base import BaseMerger



class AppendListMerger(
    BaseMerger[list[T]],
):

    plugin_type = "append_list"

    def do_merge(
        self,
        parent: list[T],
        child: list[T],
    ) -> list[T]:

        return [
            *deepcopy(parent),
            *deepcopy(child),
        ]

class ReplaceListMerger(
    BaseMerger[list[T]],
):
    """
    Replace the entire parent list.
    """

    plugin_type = "replace_list"

    def do_merge(
        self,
        parent: list[T],
        child: list[T],
    ) -> list[T]:

        return deepcopy(child)

class UniqueListMerger(
    BaseMerger[list[T]],
):

    plugin_type = "unique_list"

    def do_merge(
        self,
        parent: list[T],
        child: list[T],
    ) -> list[T]:

        result = deepcopy(parent)

        for item in child:

            if item not in result:
                result.append(
                    deepcopy(item),
                )

        return result


