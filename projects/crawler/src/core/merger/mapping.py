from copy import deepcopy
from typing import cast
from collections.abc import Callable

from core.typing.aliases import JsonDict
from .base import BaseMerger



type KeyNormalizer = Callable[[str], str]


class MappingMerger(
    BaseMerger[JsonDict],
):

    plugin_type = "mapping"

    def __init__(
        self,
        *,
        override: bool = True,
        key_normalizer: KeyNormalizer | None = None,
    ) -> None:

        self._override = override
        self._key_normalizer: KeyNormalizer = (
            key_normalizer
            or (lambda key: key)
        )

    def do_merge(
        self,
        parent: JsonDict,
        child: JsonDict,
    ) -> JsonDict:

        result = deepcopy(parent)

        index = {
            self._key_normalizer(key): key
            for key in result
        }

        for key, value in child.items():

            normalized = (
                self._key_normalizer(key)
            )

            existing_key = index.get(
                normalized,
            )

            if existing_key is not None:

                if not self._override:
                    continue

                del result[existing_key]

            result[key] = deepcopy(value)

            index[normalized] = key

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