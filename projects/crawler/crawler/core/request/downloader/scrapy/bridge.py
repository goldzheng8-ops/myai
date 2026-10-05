from __future__ import annotations
from scrapy.http import Request
from collections.abc import Mapping
from typing import Any

from core.request.descriptor import  RequestDescriptor
from core.request.downloader.serializer.scrapy import ScrapyCookieSerializer



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
        headers = dict(
            request.headers,
        )

        if request.cookies:
            cookie_header = (
                ScrapyCookieSerializer.serialize(
                    request.cookies,
                )
            )

            headers["Cookie"] = cookie_header
        return Request(
            url=request.url,
            method=request.method.value,
            headers=headers,
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