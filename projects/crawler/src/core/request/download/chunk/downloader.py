from dataclasses import replace
from typing import Any

from core.request.context import RequestContext
from core.request.download.chunk.model import ChunkRange
from core.request.download.exception import DownloadError
from core.request.download.range.model import ByteRange
from core.request.download.range.parser import RangeParser
from core.request.downloader.base import BaseDownloader
from core.extraction.response.base import ResponseAdapter


def _get_header_ci(headers: dict, name: str):
    for k, v in headers.items():
        if k.lower() == name.lower():
            return v
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
    ) -> tuple[ResponseAdapter, ByteRange, bool]:

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

        # If server returned 4xx (e.g. 404), treat it as a normal
        # response and indicate ranges are not supported so the
        # caller can handle validation/skipping.
        if 400 <= response.status_code < 500:

            total = None

            content_length = _get_header_ci(response.headers, "content-length")

            if content_length is not None:
                try:
                    total = int(content_length)
                except Exception:
                    total = None

            if total is None:
                try:
                    total = len(response.body)
                except Exception:
                    total = None

            byte_range = (
                ByteRange(start=0, end=(total - 1) if total is not None else None, total=total)
            )

            return response, byte_range, False

        # If server returned 206, expect Content-Range header.
        if response.status_code == 206:

            content_range = _get_header_ci(response.headers, "content-range")

            # Some servers may respond 206 but omit Content-Range.
            # In such cases, retry a plain GET to obtain the full
            # response and derive the total size from it.
            if content_range is None:

                # Close original probe response if it supports close
                try:
                    await response.close()
                except Exception:
                    pass

                # Retry without Range header
                headers = dict(context.descriptor.headers)
                descriptor = replace(context.descriptor, headers=headers)
                request_context = replace(context, descriptor=descriptor)

                retry_result = await self._downloader.download(request_context)

                if not retry_result.success:
                    raise DownloadError(
                        "Range probe retry failed (no Content-Range).",
                        url=context.descriptor.url,
                        cause=retry_result.error,
                    )

                retry_response = retry_result.response

                if retry_response is None:
                    raise DownloadError(
                        "Range probe retry completed without a response.",
                        url=context.descriptor.url,
                    )

                # Treat retry as full response (status 200 expected)
                if retry_response.status_code != 200:
                    raise DownloadError(
                        "Range probe retry returned unexpected status code.",
                        url=retry_response.url,
                    )

                content_length = _get_header_ci(retry_response.headers, "content-length")

                total = None

                if content_length is not None:
                    try:
                        total = int(content_length)
                    except Exception:
                        total = None

                if total is None:
                    try:
                        total = len(retry_response.body)
                    except Exception:
                        total = None

                if total is None:
                    raise DownloadError(
                        "Unable to determine total size from probe retry response.",
                        url=retry_response.url,
                    )

                byte_range = ByteRange(
                    start=0,
                    end=total - 1,
                    total=total,
                )

                return retry_response, byte_range, False

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

            return response, byte_range, True

        # Some servers ignore the Range header and return 200 with
        # the full resource. In that case, derive total size from
        # Content-Length or response body and indicate that ranges
        # are not supported so callers can fall back to a single
        # full download.
        if response.status_code == 200:

            # Try Content-Length header first
            content_length = _get_header_ci(response.headers, "content-length")

            total = None

            if content_length is not None:
                try:
                    total = int(content_length)
                except Exception:
                    total = None

            # If Content-Length missing or invalid, use body length
            if total is None:
                try:
                    total = len(response.body)
                except Exception:
                    total = None

            if total is None:
                raise DownloadError(
                    "Unable to determine total size from probe response.",
                    url=response.url,
                )

            byte_range = ByteRange(
                start=0,
                end=total - 1,
                total=total,
            )

            return response, byte_range, False

        # Any other status is an error for probe
        raise DownloadError(
            "Range probe returned unsupported status code.",
            url=response.url,
        )

    async def fetch_full(
        self,
        *,
        context: RequestContext,
    ) -> ResponseAdapter:

        # Perform a plain GET (no Range header) to retrieve full body
        headers = dict(context.descriptor.headers)

        descriptor = replace(
            context.descriptor,
            headers=headers,
        )

        request_context = replace(
            context,
            descriptor=descriptor,
        )

        result = await self._downloader.download(request_context)

        if not result.success:
            raise DownloadError(
                "Full download failed.",
                url=context.descriptor.url,
                cause=result.error,
            )

        response = result.response

        if response is None:
            raise DownloadError(
                "Full download completed without a response.",
                url=context.descriptor.url,
            )

        return response