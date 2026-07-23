

from typing import Any, Mapping

from runtime.discovery_descriptor import HttpMethod, RequestDescriptor, RequestKind, RequestProfile


class RequestDescriptorFactory:

    @classmethod
    def create(
        cls,
        *,
        url: str,
        kind: RequestKind,
        profile: RequestProfile,
        method: HttpMethod = HttpMethod.GET,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        params: Mapping[str, str] | None = None,
        body: Any = None,
        meta: Mapping[str, Any] | None = None,
    ) -> RequestDescriptor:
        ...

    @classmethod
    def detail(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        **kwargs,
    ) -> RequestDescriptor:
        return cls.create(
            url=url,
            kind=RequestKind.DETAIL,
            profile=profile,
            **kwargs,
        )

    @classmethod
    def list(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        **kwargs,
    ) -> RequestDescriptor:
        return cls.create(
            url=url,
            kind=RequestKind.LIST,
            profile=profile,
            **kwargs,
        )

    @classmethod
    def api(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        **kwargs,
    ) -> RequestDescriptor:
        return cls.create(
            url=url,
            kind=RequestKind.API,
            profile=profile,
            **kwargs,
        )

    @classmethod
    def login(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        **kwargs,
    ) -> RequestDescriptor:
        return cls.create(
            url=url,
            kind=RequestKind.LOGIN,
            profile=profile,
            **kwargs,
        )

    @classmethod
    def download(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        **kwargs,
    ) -> RequestDescriptor:
        return cls.create(
            url=url,
            kind=RequestKind.DOWNLOAD,
            profile=profile,
            **kwargs,
        )

