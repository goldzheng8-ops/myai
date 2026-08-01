

from copy import deepcopy

from models.config.request import RequestConfig
from models.runtime.request.descriptor import RequestDescriptor
from models.runtime.request.context import RequestContext
from models.runtime.merger import RequestMerger
from models.runtime.request.profile import RequestProfile
from models.runtime.spider.context import SpiderContext
from models.enums.request_kind import RequestKind

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

