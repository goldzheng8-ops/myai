from __future__ import annotations
from dataclasses import replace
from typing import Any

from core.request.download.exception import DownloadError, DownloadIncompleteError
from core.request.download.range.parser import RangeParser
from core.request.download.resume.store import ResumeStore
from core.request.download.strategy.base import DownloadStrategy
from core.extraction.response import ResponseAdapter
from core.request.downloader.result import DownloadResult
from core.request.context import RequestContext
from core.request.downloader.base import BaseDownloader
from core.request.middleware.fingerprint.provider import FingerprintProvider



class ResumableDownloadStrategy(
    DownloadStrategy,
):
    """
    Download strategy with HTTP Range-based resume support.

    The strategy stores incomplete response bodies in ResumeStore
    and resumes the download by issuing a Range request.
    """

    def __init__(
        self,
        downloader: BaseDownloader[Any],
        resume_store: ResumeStore,
        fingerprint_provider: FingerprintProvider,
        range_parser: RangeParser,
    ) -> None:
        self._downloader = downloader
        self._resume_store = resume_store
        self._fingerprint_provider = (
            fingerprint_provider
        )
        self._range_parser = range_parser
    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:

        resume_key = (
            self._fingerprint_provider.fingerprint(
                context.descriptor,
            )
        )

        downloaded = await self._resume_store.size(
            resume_key,
        )

        request_context = context

        if downloaded > 0:
            request_context = self._with_range(
                context,
                downloaded,
            )

        result = await self._downloader.download(
            request_context,
        )

        if not result.success:
            return result

        response = result.response

        if response is None:
            return self._failure(
                url=context.descriptor.url,
                error=DownloadError(
                    "Download completed without a response.",
                    url=context.descriptor.url,
                ),
                metadata=result.meta,
            )

        return await self._process_response(
            context=context,
            response=response,
            resume_key=resume_key,
            downloaded=downloaded,
            metadata=result.meta,
        )

    async def _process_response(
        self,
        *,
        context: RequestContext,
        response: ResponseAdapter,
        resume_key: str,
        downloaded: int,
        metadata: dict[str, Any],
    ) -> DownloadResult:

        status = response.status_code

        if downloaded > 0:

            if status == 206:

                await self._validate_partial_response(
                    response=response,
                    offset=downloaded,
                )

                await self._resume_store.append(
                    resume_key,
                    response.body,
                )

            elif status == 200:
                # Server ignored the Range header.
                #
                # The existing partial data can no longer
                # be combined with this response, so restart
                # the download from zero.

                await self._resume_store.delete(
                    resume_key,
                )

                await self._resume_store.append(
                    resume_key,
                    response.body,
                )

                downloaded = 0

            else:
                return self._failure(
                    url=context.descriptor.url,
                    error=DownloadError(
                        f"Unexpected HTTP status {status} "
                        "while resuming.",
                        url=context.descriptor.url,
                    ),
                    metadata=metadata,
                )

        else:

            if status not in {200, 206}:
                return self._failure(
                    url=context.descriptor.url,
                    error=DownloadError(
                        f"Unexpected HTTP status {status} "
                        "for download.",
                        url=context.descriptor.url,
                    ),
                    metadata=metadata,
                )

            await self._resume_store.append(
                resume_key,
                response.body,
            )

        total_size = await self._resume_store.size(
            resume_key,
        )

        expected_size = self._expected_size(
            response=response,
            downloaded=downloaded,
        )

        if expected_size is not None:

            if total_size > expected_size:
                return self._failure(
                    url=context.descriptor.url,
                    error=DownloadError(
                        "Downloaded data exceeds "
                        f"expected size: "
                        f"{total_size} > {expected_size}.",
                        url=context.descriptor.url,
                    ),
                    metadata=metadata,
                )

            if total_size < expected_size:
                return self._failure(
                    url=context.descriptor.url,
                    error=DownloadIncompleteError(
                        url=context.descriptor.url,
                        downloaded=total_size,
                        expected=expected_size,
                    ),
                    metadata=metadata,
                )

        body_bytes = await self._resume_store.read(
            resume_key,
        )

        await self._resume_store.delete(
            resume_key,
        )

        complete_response = response.with_body(
            body_bytes,
        )

        return DownloadResult(
            response=complete_response,
            success=True,
            meta=metadata,
        )

    async def _validate_partial_response(
        self,
        *,
        response: ResponseAdapter,
        offset: int,
    ) -> None:

        content_range = response.headers.get(
            "content-range",
        )

        if content_range is None:
            raise DownloadError(
                "Server returned 206 without "
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

        if byte_range.start != offset:
            raise DownloadError(
                "Invalid resume offset: "
                f"requested={offset}, "
                f"received={byte_range.start}.",
                url=response.url,
            )

        length = byte_range.size

        if length is None:
            raise DownloadError(
                "Content-Range does not contain "
                "a valid byte range.",
                url=response.url,
            )

        actual_size = len(
            response.body,
        )

        if actual_size != length:
            raise DownloadError(
                "Partial response size mismatch: "
                f"expected={length}, "
                f"actual={actual_size}.",
                url=response.url,
            )

    def _with_range(
        self,
        context: RequestContext,
        offset: int,
    ) -> RequestContext:

        descriptor = context.descriptor

        headers = dict(
            descriptor.headers,
        )

        headers["Range"] = (
            self._range_parser.build_range(
                offset,
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

    def _expected_size(
        self,
        *,
        response: ResponseAdapter,
        downloaded: int,
    ) -> int | None:

        content_range = response.headers.get(
            "content-range",
        )

        if content_range:

            byte_range = (
                self._range_parser.parse_content_range(
                    content_range,
                )
            )

            if (
                byte_range is not None
                and byte_range.total is not None
            ):
                return byte_range.total

        content_length = response.headers.get(
            "content-length",
        )

        if content_length is None:
            return None

        try:
            length = int(content_length)
        except ValueError:
            return None

        if length < 0:
            return None

        # When resuming, Content-Length represents
        # the remaining response body.
        if downloaded > 0:
            return downloaded + length

        return length

    @staticmethod
    def _failure(
        *,
        url: str,
        error: Exception,
        metadata: dict[str, Any],
    ) -> DownloadResult:

        return DownloadResult(
            success=False,
            error=error,
            meta=metadata,
        )