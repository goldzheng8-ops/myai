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

        for key, value in child.items():

            if (

                key in result

                and isinstance(
                    result[key],
                    dict,
                )

                and isinstance(
                    value,
                    dict,
                )

            ):

                left = cast(
                    JsonDict,
                    result[key],
                )

                right = cast(
                    JsonDict,
                    value,
                )

                result[key] = self.do_merge(
                    left,
                    right,
                )

            else:

                result[key] = deepcopy(value)

        return result