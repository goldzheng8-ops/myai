from __future__ import annotations
import asyncio

from core.request.downloader.aria2.model import Aria2DownloadResult, Aria2Status

from .client import Aria2Client


class Aria2DownloadMonitor:

    def __init__(
        self,
        client: Aria2Client,
        *,
        poll_interval: float = 0.5,
        timeout: float | None = None,
    ) -> None:

        if poll_interval <= 0:
            raise ValueError(
                "poll_interval must be greater than zero.",
            )

        if (
            timeout is not None
            and timeout <= 0
        ):
            raise ValueError(
                "timeout must be greater than zero.",
            )

        self._client = client
        self._poll_interval = poll_interval
        self._timeout = timeout

    async def wait(
        self,
        gid: str,
    ) -> Aria2DownloadResult:

        loop = asyncio.get_running_loop()

        started_at = loop.time()

        while True:

            status = await self._client.tell_status(
                gid,
            )

            if status.status in {
                Aria2Status.COMPLETE,
                Aria2Status.ERROR,
                Aria2Status.REMOVED,
            }:

                return Aria2DownloadResult(
                    gid=gid,
                    status=status,
                    files=status.files,
                    error_code=status.error_code,
                    error_message=status.error_message,
                )

            if (
                self._timeout is not None
                and loop.time() - started_at
                >= self._timeout
            ):
                raise TimeoutError(
                    "Aria2 download timed out: "
                    f"gid={gid!r}",
                )

            await asyncio.sleep(
                self._poll_interval,
            )