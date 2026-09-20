from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ByteRange:
    """
    A byte range parsed from an HTTP Range header
    or Content-Range header.

    start and end are inclusive.
    """

    start: int | None
    end: int | None
    total: int | None = None

    @property
    def size(self) -> int | None:
        if self.start is None or self.end is None:
            return None

        return self.end - self.start + 1

    @property
    def is_open_ended(self) -> bool:
        return (
            self.start is not None
            and self.end is None
        )

    @property
    def is_unsatisfied(self) -> bool:
        return (
            self.start is None
            and self.end is None
        )