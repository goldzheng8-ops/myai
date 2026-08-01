from copy import deepcopy
from typing import Any, Mapping, TypeVar

from .base import BaseMerger

T = TypeVar("T")


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
    """
    Append child items while preserving order
    and removing duplicates.
    """

    plugin_type = "unique_list"

    def do_merge(
        self,
        parent: list[T],
        child: list[T],
    ) -> list[T]:

        result = deepcopy(parent)

        seen = set(result)

        for item in child:
            if item not in seen:
                seen.add(item)
                result.append(deepcopy(item))

        return result

class KeyedListMerger(
    BaseMerger[list[Mapping[str, Any]]],
):

    plugin_type = "keyed_list"
    
    def __init__(
        self,
        key: str,
    ) -> None:

        self._key = key

    def do_merge(

        self,

        parent:list[Mapping[str, Any]],

        child:list[Mapping[str, Any]] 

    )->list[Mapping[str, Any]]:

        result = deepcopy(parent)

        index = {

            item[self._key]: i

            for i, item in enumerate(result)

        }

        for item in child:

            value = item[self._key]

            if value in index:

                result[
                    index[value]
                ] = deepcopy(item)

            else:

                index[value] = len(result)

                result.append(
                    deepcopy(item)
                )

        return result