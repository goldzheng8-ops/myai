from copy import deepcopy

from core.typing.aliases import JsonDict
from .base import BaseMerger


from typing import cast


class MappingMerger(
    BaseMerger[JsonDict],
):

    plugin_type = "mapping"

    def do_merge(
        self,
        parent: JsonDict,
        child: JsonDict,
    ) -> JsonDict:

        result = deepcopy(parent)

        result.update(
            deepcopy(child),
        )

        return result

class RecursiveMappingMerger(
    BaseMerger[JsonDict],
):

    plugin_type = "recursive_mapping"

    def do_merge(

        self,

        parent: JsonDict,

        child: JsonDict,

    )-> JsonDict:

        result = deepcopy(parent)

        for key, child_value in child.items():
            parent_value = result.get(key)
            if (

                key in result

                and isinstance(
                    parent_value,
                    dict,
                )

                and isinstance(
                    child_value,
                    dict,
                )

            ):

                left = cast(
                    JsonDict,
                    parent_value,
                )

                right = cast(
                    JsonDict,
                    child_value,
                )

                result[key] = self.do_merge(
                    left,
                    right,
                )

            else:

                result[key] = deepcopy(child_value)

        return result