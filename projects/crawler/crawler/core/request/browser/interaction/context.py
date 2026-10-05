from dataclasses import dataclass
from typing import Generic, TypeVar

from core.request.browser.runtime_manager import BrowserSessionRuntime
from core.request.context import RequestContext
from core.spider.config import SpiderConfig

ConfigT = TypeVar(
    "ConfigT",
    bound=SpiderConfig,
)


@dataclass(slots=True)
class BrowserInteractionContext(
    Generic[ConfigT],
):

    request: RequestContext

    config: ConfigT

    session_runtime:BrowserSessionRuntime
