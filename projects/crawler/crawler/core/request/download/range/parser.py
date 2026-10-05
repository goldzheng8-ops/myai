import re

from core.request.download.range.model import ByteRange


class RangeParser:

    _RANGE_PATTERN = re.compile(
        r"^bytes=(\d+)-(\d*)$",
        re.IGNORECASE,
    )

    _CONTENT_RANGE_PATTERN = re.compile(
        r"^bytes\s+"
        r"(?:(\d+)-(\d+)|\*)"
        r"/"
        r"(\d+|\*)$",
        re.IGNORECASE,
    )

    @classmethod
    def parse_range(
        cls,
        value: str,
    ) -> ByteRange | None:

        value = value.strip()

        match = cls._RANGE_PATTERN.fullmatch(
            value,
        )

        if match is None:
            return None

        start = int(match.group(1))

        end_text = match.group(2)

        end = (
            int(end_text)
            if end_text
            else None
        )

        if end is not None and end < start:
            return None

        return ByteRange(
            start=start,
            end=end,
            total=None,
        )

    @classmethod
    def parse_content_range(
        cls,
        value: str,
    ) -> ByteRange | None:

        value = value.strip()

        match = cls._CONTENT_RANGE_PATTERN.fullmatch(
            value,
        )

        if match is None:
            return None

        start_text = match.group(1)
        end_text = match.group(2)
        total_text = match.group(3)

        start = (
            int(start_text)
            if start_text is not None
            else None
        )

        end = (
            int(end_text)
            if end_text is not None
            else None
        )

        total = (
            int(total_text)
            if total_text != "*"
            else None
        )

        if (
            start is not None
            and end is not None
            and start > end
        ):
            return None

        if (
            total is not None
            and start is not None
            and end is not None
            and end >= total
        ):
            return None

        return ByteRange(
            start=start,
            end=end,
            total=total,
        )

    @staticmethod
    def build_range(
        start: int,
        end: int | None = None,
    ) -> str:

        if start < 0:
            raise ValueError(
                "Range start must be non-negative.",
            )

        if end is not None and end < start:
            raise ValueError(
                "Range end must be greater than "
                "or equal to start.",
            )

        if end is None:
            return f"bytes={start}-"

        return f"bytes={start}-{end}"