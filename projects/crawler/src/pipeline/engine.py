

from adapters.base import ResponseAdapter
from request.base import RequestMiddleware
from request.context import RequestContext



class RequestPipeline:

    def __init__(
        self,
        middlewares: list[RequestMiddleware],
    ):
        self.middlewares = middlewares

    def process_request(
    self,
    request: RequestContext,
    ) -> RequestContext:

        current = request

        for middleware in self.middlewares:

            current = middleware.process_request(current)

        return current

    def process_response(
        self,
        request:RequestContext,
        response:ResponseAdapter,
    ):

        current = response

        for middleware in reversed(self.middlewares):

            current = middleware.process_response(
                request,
                current,
            )

        return current
    
    def process_exception(
        self,
        request:RequestContext,
        exception: Exception,
    ):

        current = exception

        for middleware in reversed(self.middlewares):

            current = middleware.process_exception(
                request,
                current,
            )

        return current


