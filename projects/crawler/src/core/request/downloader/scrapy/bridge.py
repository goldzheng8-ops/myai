from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.request.descriptor import RequestDescriptor
from scrapy import Request

from core.request.context import RequestContext


class ScrapyRequestBridge:
    """
    Converts an application RequestContext into
    a native Scrapy Request.
    """

    def build(
        self,
        context: RequestContext,
    ) -> Request:
        request = context.descriptor
        meta = request.meta

        return Request(
            url=request.url,
            method=request.method.value,
            headers=self._build_headers(
                request.headers,
            ),
            cookies=self._build_cookies(
                request.cookies,
            ),
            body=request.body or b"",
            priority=meta.priority,
            dont_filter=meta.dont_filter,
            meta=self._build_meta(
                request,
            ),
            cb_kwargs={
                "request_context": context,
            },
        )

    @staticmethod
    def _build_headers(
        headers: Mapping[str, str],
    ) -> dict[str, str]:
        return {
            str(name): str(value)
            for name, value in headers.items()
        }

    @staticmethod
    def _build_cookies(
        cookies: Mapping[str, str],
    ) -> dict[str | bytes, str | bytes]:
        return {
            name: value
            for name, value in cookies.items()
        }

    @staticmethod
    def _build_meta(
        request: RequestDescriptor,
    ) -> dict[str, Any]:
        """
        Build Scrapy's request.meta.

        Framework control data should not be copied blindly
        into Scrapy meta. Only data explicitly intended for
        Scrapy/runtime integration belongs here.
        """
        meta = dict[str, Any]()

        proxy = request.proxy

        if proxy is not None:
            meta["proxy"] = proxy.as_url()

        return meta