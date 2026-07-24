from copy import deepcopy
from typing import Any

from config.discovery.base import RequestPatch


class RequestPatchRenderer:

    @classmethod
    def render(
        cls,
        patch: RequestPatch,
        **variables: Any,
    ) -> RequestPatch:

        return RequestPatch(
            url=cls._render(patch.url, variables),
            params=cls._render(patch.params, variables),
            body=cls._render(patch.body, variables),
        )

    @classmethod
    def _render(
        cls,
        value: Any,
        variables: dict[str, Any],
    ) -> Any:

        if isinstance(value, str):
            return value.format(**variables)

        if isinstance(value, dict):
            return {
                k: cls._render(v, variables)
                for k, v in value.items()
            }

        if isinstance(value, list):
            return [
                cls._render(v, variables)
                for v in value
            ]

        return deepcopy(value)