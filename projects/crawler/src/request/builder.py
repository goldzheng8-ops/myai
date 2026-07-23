

from copy import deepcopy

from config.request import RequestConfig
from runtime.discovery_descriptor import RequestDescriptor
from runtime.request_context import RequestContext, RequestKind
from request.merger import RequestMerger
from runtime.request_profile import RequestProfile
from runtime.spider_context import SpiderContext


class RequestBuilder:

    def __init__(
        self,
        merger: RequestMerger,
    ):
        self._merger = merger

    def build_start(
        self,
        spider: SpiderContext,
        request: RequestConfig,
        *,
        kind:RequestKind,
        profile: RequestProfile,
    ) -> RequestContext:
        """
        构建 Spider 的第一个 Request。
        """

        return RequestContext(
            spider=spider,
            request=request.model_copy(deep=True),
            kind=kind,
            profile=profile,
        )

    def build(
        self,
        parent: RequestContext,
        descriptor: RequestDescriptor,
    ) -> RequestContext:
        """
        根据父 Request 构建新的 Request。
        """

        request = self._merger.merge(
            parent.request,
            descriptor,
        )

        return RequestContext(
            spider=parent.spider,
            request=request,
            kind=descriptor.kind or parent.kind,
            profile=descriptor.profile or parent.profile,
            meta=deepcopy(parent.meta)
            if descriptor.meta is None
            else deepcopy(descriptor.meta),
        )

    def clone(
        self,
        context: RequestContext,
    ) -> RequestContext:
        """
        深拷贝 RequestContext。
        """

        return RequestContext(
            spider=context.spider,
            request=context.request.model_copy(deep=True),
            kind=context.kind,
            profile=context.profile,
            meta=deepcopy(context.meta),
        )

