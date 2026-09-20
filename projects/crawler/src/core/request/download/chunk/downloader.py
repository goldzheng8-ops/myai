from dataclasses import replace
from typing import Any

from core.request.context import RequestContext
from core.request.download.chunk.model import ChunkRange
from core.request.download.exception import DownloadError
from core.request.download.range.model import ByteRange
from core.request.download.range.parser import RangeParser
from core.request.downloader.base import BaseDownloader
from core.extraction.response.base import ResponseAdapter

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

        headers = dict(
            context.descriptor.headers,
        )

        headers["Range"] = (
            self._range_parser.build_range(
                chunk.start,
                chunk.end,
            )
        )

        descriptor = replace(
            context.descriptor,
            headers=headers,
        )

        request_context = replace(
            context,
            descriptor=descriptor,
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

    def _validate_response(
        self,
        *,
        response: ResponseAdapter,
        chunk: ChunkRange,
    ) -> ByteRange:

        if response.status_code != 206:
            raise DownloadError(
                f"Expected HTTP 206 for chunk, "
                f"got {response.status_code}.",
                url=response.url,
            )

        content_range = response.headers.get(
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
                f"Invalid Content-Range: "
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
    ) -> tuple[ResponseAdapter, ByteRange]:

        headers = dict(
            context.descriptor.headers,
        )

        headers["Range"] = "bytes=0-0"

        descriptor = replace(
            context.descriptor,
            headers=headers,
        )

        request_context = replace(
            context,
            descriptor=descriptor,
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

        if response.status_code != 206:
            raise DownloadError(
                "Server does not support the required "
                "range request.",
                url=response.url,
            )

        content_range = response.headers.get(
            "content-range",
        )

        if content_range is None:
            raise DownloadError(
                "Range probe response does not contain "
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
                f"Invalid Content-Range: "
                f"{content_range!r}",
                url=response.url,
            )

        if byte_range.start != 0:
            raise DownloadError(
                "Range probe returned an unexpected "
                "start offset.",
                url=response.url,
            )

        return response, byte_range