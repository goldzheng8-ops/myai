from collections.abc import Sequence

from core.output.model import OutputItem
from core.output.resolver import OutputResolver


class OutputEngine:

    def __init__(
        self,
        output_resolver: OutputResolver,
    ) -> None:
        self._resolver = output_resolver

    async def write(
        self,
        item: OutputItem,
        outputs: Sequence[str],
    ) -> None:

        for name in outputs:
            sink = self._resolver.resolve(name)
            await sink.write(item)