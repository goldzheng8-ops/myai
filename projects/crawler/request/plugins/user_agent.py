

from request.base import RequestMiddleware
from request.context import RequestContext



class UserAgentMiddleware(RequestMiddleware):

    def process_request(self, request: RequestContext) -> RequestContext:

        request.headers["User-Agent"] = ...

        return request