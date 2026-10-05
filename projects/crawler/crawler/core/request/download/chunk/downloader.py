from collections.abc import Mapping
from dataclasses import replace
from typing import Any

from core.extraction.response.base import ResponseAdapter
from core.request.context import RequestContext
from core.request.download.chunk.model import ChunkRange
from core.request.download.exception import DownloadError
from core.request.download.range.model import ByteRange
from core.request.download.range.parser import RangeParser
from core.request.downloader.base import BaseDownloader


def _get_header_ci(
    headers: Mapping[str, str],
    name: str,
) -> str | None:

    name = name.lower()

    for key, value in headers.items():
        if key.lower() == name:
            return value

    return None


class ChunkDownloader:

    def __init__(
        self,
        downloader: BaseDownloader[Any],
        range_parser: RangeParser,
    ) -> None:

        self._downloader = downloader
        self._range_parser = range_parser

    async def download(
        self,
        *,
        context: RequestContext,
        chunk: ChunkRange,
    ) -> ResponseAdapter:

        request_context = self._with_range(
            context=context,
            start=chunk.start,
            end=chunk.end,
        )

        result = await self._downloader.download(
            request_context,
        )

        if not result.success:
            raise DownloadError(
                "Chunk download failed.",
                url=context.descriptor.url,
                cause=result.error,
            )

        response = result.response

        if response is None:
            raise DownloadError(
                "Chunk download completed "
                "without a response.",
                url=context.descriptor.url,
            )

        self._validate_response(
            response=response,
            chunk=chunk,
        )

        return response

    def _with_range(
        self,
        *,
        context: RequestContext,
        start: int,
        end: int | None = None,
    ) -> RequestContext:

        descriptor = context.descriptor

        headers = dict(
            descriptor.headers,
        )

        headers["Range"] = (
            self._range_parser.build_range(
                start,
                end,
            )
        )

        descriptor = replace(
            descriptor,
            headers=headers,
        )

        return replace(
            context,
            descriptor=descriptor,
        )

    def _validate_response(
        self,
        *,
        response: ResponseAdapter,
        chunk: ChunkRange,
    ) -> ByteRange:

        if response.status_code != 206:
            raise DownloadError(
                "Expected HTTP 206 for chunk, "
                f"got {response.status_code}.",
                url=response.url,
            )

        content_range = _get_header_ci(
            response.headers,
            "content-range",
        )

        if content_range is None:
            raise DownloadError(
                "Chunk response does not contain "
                "Content-Range.",
                url=response.url,
            )

        byte_range = (
            self._range_parser.parse_content_range(
                content_range,
            )
        )

        if byte_range is None:
            raise DownloadError(
                "Invalid Content-Range: "
                f"{content_range!r}",
                url=response.url,
            )

        if byte_range.start != chunk.start:
            raise DownloadError(
                "Chunk response start mismatch: "
                f"expected={chunk.start}, "
                f"actual={byte_range.start}.",
                url=response.url,
            )

        if byte_range.end != chunk.end:
            raise DownloadError(
                "Chunk response end mismatch: "
                f"expected={chunk.end}, "
                f"actual={byte_range.end}.",
                url=response.url,
            )

        actual_size = len(response.body)

        if actual_size != chunk.size:
            raise DownloadError(
                "Chunk response size mismatch: "
                f"expected={chunk.size}, "
                f"actual={actual_size}.",
                url=response.url,
            )

        return byte_range

    async def probe(
        self,
        *,
        context: RequestContext,
    ) -> tuple[
        ResponseAdapter,
        ByteRange,
        bool,
    ]:

        request_context = self._with_range(
            context=context,
            start=0,
            end=0,
        )

        result = await self._downloader.download(
            request_context,
        )

        if not result.success:
            raise DownloadError(
                "Range probe failed.",
                url=context.descriptor.url,
                cause=result.error,
            )

        response = result.response

        if response is None:
            raise DownloadError(
                "Range probe completed "
                "without a response.",
                url=context.descriptor.url,
            )

        status = response.status_code

        if status == 206:
            return await self._process_partial_probe(
                context=context,
                response=response,
            )

        if status == 200:
            return (
                response,
                self._build_full_range(response),
                False,
            )

        if 400 <= status < 500:
            return (
                response,
                self._build_error_range(response),
                False,
            )

        raise DownloadError(
            "Range probe returned unsupported "
            f"status code: {status}.",
            url=response.url,
        )

    async def _process_partial_probe(
        self,
        *,
        context: RequestContext,
        response: ResponseAdapter,
    ) -> tuple[
        ResponseAdapter,
        ByteRange,
        bool,
    ]:

        content_range = _get_header_ci(
            response.headers,
            "content-range",
        )

        if content_range is not None:
            byte_range = (
                self._range_parser.parse_content_range(
                    content_range,
                )
            )

            if byte_range is None:
                raise DownloadError(
                    "Invalid Content-Range: "
                    f"{content_range!r}",
                    url=response.url,
                )

            if byte_range.start != 0:
                raise DownloadError(
                    "Range probe returned an "
                    "unexpected start offset.",
                    url=response.url,
                )

            return (
                response,
                byte_range,
                True,
            )

        return await self._retry_full_probe(
            context=context,
            response=response,
        )

    async def _retry_full_probe(
        self,
        *,
        context: RequestContext,
        response: ResponseAdapter,
    ) -> tuple[
        ResponseAdapter,
        ByteRange,
        bool,
    ]:

        await response.close()

        result = await self._downloader.download(
            self._without_range(context),
        )

        if not result.success:
            raise DownloadError(
                "Range probe retry failed "
                "(no Content-Range).",
                url=context.descriptor.url,
                cause=result.error,
            )

        retry_response = result.response

        if retry_response is None:
            raise DownloadError(
                "Range probe retry completed "
                "without a response.",
                url=context.descriptor.url,
            )

        if retry_response.status_code != 200:
            raise DownloadError(
                "Range probe retry returned "
                f"unexpected status code: "
                f"{retry_response.status_code}.",
                url=retry_response.url,
            )

        total = self._resolve_total_size(
            retry_response,
        )

        if total is None:
            raise DownloadError(
                "Unable to determine total size "
                "from probe retry response.",
                url=retry_response.url,
            )

        return (
            retry_response,
            ByteRange(
                start=0,
                end=total - 1,
                total=total,
            ),
            False,
        )

    def _without_range(
        self,
        context: RequestContext,
    ) -> RequestContext:

        descriptor = context.descriptor

        headers = {
            key: value
            for key, value in descriptor.headers.items()
            if key.lower() != "range"
        }

        descriptor = replace(
            descriptor,
            headers=headers,
        )

        return replace(
            context,
            descriptor=descriptor,
        )

    @staticmethod
    def _parse_content_length(
        headers: Mapping[str, str],
    ) -> int | None:

        value = _get_header_ci(
            headers,
            "content-length",
        )

        if value is None:
            return None

        try:
            length = int(value)
        except ValueError:
            return None

        if length < 0:
            return None

        return length

    @classmethod
    def _resolve_total_size(
        cls,
        response: ResponseAdapter,
    ) -> int | None:

        total = cls._parse_content_length(
            response.headers,
        )

        if total is not None:
            return total

        return len(response.body)

    @classmethod
    def _build_full_range(
        cls,
        response: ResponseAdapter,
    ) -> ByteRange:

        total = cls._resolve_total_size(
            response,
        )

        if total is None:
            raise DownloadError(
                "Unable to determine total size "
                "from probe response.",
                url=response.url,
            )

        if total == 0:
            return ByteRange(
                start=0,
                end=None,
                total=0,
            )

        return ByteRange(
            start=0,
            end=total - 1,
            total=total,
        )

    @classmethod
    def _build_error_range(
        cls,
        response: ResponseAdapter,
    ) -> ByteRange:

        total = cls._resolve_total_size(
            response,
        )

        if total is None:
            return ByteRange(
                start=0,
                end=None,
                total=None,
            )

        if total == 0:
            return ByteRange(
                start=0,
                end=None,
                total=0,
            )

        return ByteRange(
            start=0,
            end=total - 1,
            total=total,
        )

    async def fetch_full(
        self,
        *,
        context: RequestContext,
    ) -> ResponseAdapter:

        result = await self._downloader.download(
            self._without_range(context),
        )

        if not result.success:
            raise DownloadError(
                "Full download failed.",
                url=context.descriptor.url,
                cause=result.error,
            )

        response = result.response

        if response is None:
            raise DownloadError(
                "Full download completed "
                "without a response.",
                url=context.descriptor.url,
            )

        return response