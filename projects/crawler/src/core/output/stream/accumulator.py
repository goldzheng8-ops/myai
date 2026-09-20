from collections.abc import AsyncIterable, AsyncIterator


class StreamChunkAccumulator:
    """
    Accumulates arbitrary stream chunks into chunks of at least
    the configured target size.

    The final emitted chunk may be smaller than target_size.
    """

    def __init__(
        self,
        target_size: int,
    ) -> None:

        if target_size <= 0:
            raise ValueError(
                "target_size must be greater than zero.",
            )

        self._target_size = target_size

    async def accumulate(
        self,
        source: AsyncIterable[bytes],
    ) -> AsyncIterator[bytes]:

        buffer = bytearray()

        async for chunk in source:

            if not chunk:
                continue

            buffer.extend(chunk)

            while len(buffer) >= self._target_size:

                yield bytes(
                    buffer[
                        :self._target_size
                    ],
                )

                del buffer[
                    :self._target_size
                ]

        if buffer:
            yield bytes(buffer)