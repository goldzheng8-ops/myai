from abc import ABC
from abc import abstractmethod

from .context import RequestContext


class RequestMiddleware(ABC):

    @abstractmethod
    def process_request(
        self,
        request: RequestContext,
    ) -> RequestContext:
        """
        下载之前
        """
        raise NotImplementedError

    def process_response(
        self,
        request: RequestContext,
        response,
    ):
        """
        下载之后
        """
        return response

    def process_exception(
        self,
        request: RequestContext,
        exception: Exception,
    ):
        """
        下载异常
        """
        return None