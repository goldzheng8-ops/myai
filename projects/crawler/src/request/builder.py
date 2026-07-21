from __future__ import annotations

from copy import deepcopy

from config.config import RequestConfig

from .context import RequestContext


class RequestBuilder:

    def __init__(self) -> None:

        self._request = RequestContext(url="")

    def from_config(
        self,
        config: RequestConfig,
    ) -> "RequestBuilder":

        self._request.url = config.url
        self._request.method = config.method
        self._request.headers = deepcopy(config.headers)
        self._request.cookies = deepcopy(config.cookies)
        self._request.params = deepcopy(config.params)
        self._request.body = config.body
        self._request.timeout = config.timeout

        return self

    def with_headers(
        self,
        headers: dict[str, str],
    ) -> "RequestBuilder":

        self._request.headers.update(headers)

        return self

    def with_params(
        self,
        params: dict[str, Any],
    ) -> "RequestBuilder":

        self._request.params.update(params)

        return self

    def with_meta(
        self,
        meta: dict[str, Any],
    ) -> "RequestBuilder":

        self._request.meta.update(meta)

        return self

    def with_retry(
        self,
        retry: int,
    ) -> "RequestBuilder":

        self._request.retry = retry

        return self

    def with_priority(
        self,
        priority: int,
    ) -> "RequestBuilder":

        self._request.priority = priority

        return self

    def with_proxy(
        self,
        proxy: str,
    ) -> "RequestBuilder":

        self._request.proxy = proxy

        return self

    def build(self) -> RequestContext:

        return deepcopy(self._request)