
from config.manager import ConfigManager 
from config.config import RequestConfig
from downloader.base import RequestContext
from task.model import Task


class TaskContextFactory:

    def __init__(
        self,
        crawler_manager: ConfigManager,
    ):
        self.crawler_manager = crawler_manager

    def create(
        self,
        task: Task,
    ) -> RequestContext:

        crawler = self.crawler_manager.get(task.crawler)

        request = RequestConfig(
            url=task.request.url,
            headers=task.request.headers,
            cookies=task.request.cookies,
            params=task.request.params,
            body=task.request.body,
        )

        return RequestContext(
            request=request,
            crawler=crawler,
            meta={},
            retry=0,
        )