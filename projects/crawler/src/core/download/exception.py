from __future__ import annotations
from core.exception.application import CrawlerError

class DownloadError(CrawlerError):
    """
    Base exception for download failures.
    """

    def __init__(
        self,
        message: str,
        *,
        url: str | None = None,
        cause: BaseException | None = None,
    ) -> None:

        super().__init__(message)

        self.url = url
        self.cause = cause

        if cause is not None:
            self.__cause__ = cause


class DownloadIncompleteError(
    DownloadError,
):
    """
    Raised when a resumable download has not
    reached its expected total size.
    """

    def __init__(
        self,
        *,
        url: str,
        downloaded: int,
        expected: int | None = None,
    ) -> None:

        self.downloaded = downloaded
        self.expected = expected

        if expected is None:
            message = (
                f"Download incomplete: {url!r}; "
                f"downloaded={downloaded}"
            )
        else:
            message = (
                f"Download incomplete: {url!r}; "
                f"downloaded={downloaded}, "
                f"expected={expected}"
            )

        super().__init__(
            message,
            url=url,
        )