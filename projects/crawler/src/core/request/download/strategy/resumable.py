from __future__ import annotations
import re
from dataclasses import replace
from typing import Any

from core.request.download.exception import DownloadError, DownloadIncompleteError
from core.request.download.resume.base import ResumeStore
from core.request.download.strategy.base import DownloadStrategy
from core.extraction.response import ResponseAdapter
from core.request.downloader.result import DownloadResult
from core.request.context import RequestContext
from core.request.downloader.base import BaseDownloader
from core.request.middleware.fingerprint.provider import FingerprintProvider



class ResumableDownloadStrategy(
    DownloadStrategy,
):

    def __init__(
        self,
        downloader: BaseDownloader[Any],
        resume_store: ResumeStore,
        fingerprint_provider: FingerprintProvider,
    ) -> None:

        self._downloader = downloader
        self._resume_store = resume_store
        self._fingerprint_provider = (
            fingerprint_provider
        )

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

        # if not result.success:
        #     raise DownloadError(
        #         "Download failed.",
        #         url=context.descriptor.url,
        #         cause=result.error,
        #     )
        if not result.success:
            return result

        response = result.response

        # if response is None:
        #     raise DownloadError(
        #         "Download completed without a response.",
        #         url=context.descriptor.url,
        #     )
        if response is None:
            return DownloadResult(
                success=False,
                error=DownloadError(
                    "Download completed without a response.",
                    url=context.descriptor.url,
                ),
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
                # Server ignored Range.
                #
                # The existing partial file is no longer
                # compatible with this response, so restart
                # the download from zero.
                await self._resume_store.delete(
                    resume_key,
                )

                await self._resume_store.append(
                    resume_key,
                    response.body,
                )

            else:
                # raise DownloadError(
                #     f"Unexpected HTTP status {status} "
                #     f"while resuming.",
                #     url=context.descriptor.url,
                # )
                return DownloadResult(
                    success=False,
                    error=DownloadError(
                        f"Unexpected HTTP status {status} "
                        f"while resuming.",
                        url=context.descriptor.url,
                    ),
                    meta=metadata,
                )       

        else:

            if status not in {200, 206}:
                # raise DownloadError(
                #     f"Unexpected HTTP status {status} "
                #     f"for download.",
                #     url=context.descriptor.url,
                # )
                return DownloadResult(
                    success=False,
                    error=DownloadError(
                        f"Unexpected HTTP status {status} "
                        f"for download.",
                        url=context.descriptor.url,
                    ),
                    meta=metadata,
                )

            await self._resume_store.append(
                resume_key,
                response.body,
            )

        total_size = (
            await self._resume_store.size(
                resume_key,
            )
        )

        expected = self._expected_size(
            response=response,
            downloaded=downloaded,
        )

        if expected is not None:

            if total_size > expected:
                # raise DownloadError(
                #     f"Downloaded data exceeds expected "
                #     f"size: {total_size} > {expected}.",
                #     url=context.descriptor.url,
                # )
                return DownloadResult(
                    success=False,
                    error=DownloadError(
                        "Downloaded data exceeds "
                        f"expected size: "
                        f"{total_size} > {expected}.",
                        url=context.descriptor.url,
                    ),
                    meta=metadata,
                )

            if total_size < expected:
                # raise DownloadIncompleteError(
                #     url=context.descriptor.url,
                #     downloaded=total_size,
                #     expected=expected,
                # )
                return DownloadResult(
                    success=False,
                    error=DownloadIncompleteError(
                        url=context.descriptor.url,
                        downloaded=total_size,
                        expected=expected,
                    ),
                    meta=metadata,
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

        range_start = self._parse_range_start(
            content_range,
        )

        if range_start is None:
            raise DownloadError(
                f"Invalid Content-Range: "
                f"{content_range!r}",
                url=response.url,
            )

        if range_start != offset:
            raise DownloadError(
                "Invalid resume offset: "
                f"requested={offset}, "
                f"received={range_start}.",
                url=response.url,
            )

        expected_chunk_size = (
            self._parse_range_chunk_size(
                content_range,
            )
        )

        if expected_chunk_size is not None:

            actual_chunk_size = len(
                response.body,
            )

            if actual_chunk_size != expected_chunk_size:
                raise DownloadError(
                    "Partial response size mismatch: "
                    f"expected={expected_chunk_size}, "
                    f"actual={actual_chunk_size}.",
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
            f"bytes={offset}-"
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

            total = self._parse_total_size(
                content_range,
            )

            if total is not None:
                return total

        content_length = response.headers.get(
            "content-length",
        )

        if content_length is None:
            return None

        try:
            length = int(content_length)
        except ValueError:
            return None

        # When resuming, Content-Length describes
        # the remaining response body, not the whole file.
        if downloaded > 0:
            return downloaded + length

        return length

    @staticmethod
    def _parse_total_size(
        value: str,
    ) -> int | None:

        if "/" not in value:
            return None

        total = value.rsplit(
            "/",
            1,
        )[1].strip()

        if total == "*":
            return None

        try:
            return int(total)
        except ValueError:
            return None

    @staticmethod
    def _parse_range_start(
        value: str,
    ) -> int | None:

        match = re.fullmatch(
            r"bytes\s+(\d+)-(\d+)/(\d+|\*)",
            value.strip(),
        )

        if match is None:
            return None

        return int(match.group(1))

    @staticmethod
    def _parse_range_chunk_size(
        value: str,
    ) -> int | None:

        match = re.fullmatch(
            r"bytes\s+(\d+)-(\d+)/(\d+|\*)",
            value.strip(),
        )

        if match is None:
            return None

        start = int(match.group(1))
        end = int(match.group(2))

        return end - start + 1