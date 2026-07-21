from __future__ import annotations

from abc import ABC, abstractmethod

from request.context import RequestContext


class BaseRunner(ABC):

    async def start(self) -> None:
        """初始化 Runner。"""
        return

    async def close(self) -> None:
        """释放 Runner 资源。"""
        return

    @abstractmethod
    async def run(self, context: RequestContext):
        """执行一次爬虫任务。"""
        ...