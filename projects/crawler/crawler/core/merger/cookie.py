from core.merger.base import BaseMerger
from core.request.middleware.cookie.model import Cookie


class CookieMerger(
    BaseMerger[tuple[Cookie, ...]],
):
    plugin_type = "cookie"

    def __init__(
        self,
        *,
        override: bool = True,
    ) -> None:
        self._override = override

    def do_merge(
        self,
        parent: tuple[Cookie, ...],
        child: tuple[Cookie, ...],
    ) -> tuple[Cookie, ...]:

        result = list(parent)

        index = {
            cookie.identity(): index
            for index, cookie in enumerate(result)
        }

        for cookie in child:

            key = cookie.identity()

            existing_index = index.get(key)

            if existing_index is not None:

                if self._override:
                    result[existing_index] = cookie

            else:

                index[key] = len(result)
                result.append(cookie)

        return tuple(result)