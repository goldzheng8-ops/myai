from copy import deepcopy

from .base import BaseMerger
from core.typing.aliases import JsonDict

class KeyedListMerger(
    BaseMerger[
        list[JsonDict]
    ],
):

    plugin_type = "keyed_list"

    def __init__(
        self,
        key: str,
        item_merger: BaseMerger[
            JsonDict
        ] | None = None,
    ) -> None:

        self._key = key
        self._item_merger = item_merger

    def do_merge(
        self,
        parent: list[JsonDict],
        child: list[JsonDict],
    ) -> list[JsonDict]:

        result = deepcopy(parent)

        index = {
            item[self._key]: i
            for i, item in enumerate(result)
        }

        for item in child:

            key = item[self._key]

            if key not in index:

                index[key] = len(result)

                result.append(
                    deepcopy(item),
                )

                continue

            position = index[key]

            if self._item_merger is None:

                result[position] = deepcopy(
                    item,
                )

            else:

                result[position] = (
                    self._item_merger.merge(
                        result[position],
                        item,
                    )
                )

        return result