from __future__ import annotations

from abc import ABC
from typing import Generic

from core.lifecycle.protocol import LifecycleParticipant
from core.request.context import RequestContext


from .plugin import DownloaderPlugin
from .request import DownloadRequest

from .typing import ConfigT




class BaseDownloader(
    LifecycleParticipant,
    DownloaderPlugin,
    Generic[ConfigT],
    ABC,
):
    """
    Base implementation shared by concrete downloaders.
    """

    def __init__(
        self,
        config: ConfigT,
    ) -> None:

        self._config = config

    @property
    def config(
        self,
    ) -> ConfigT:

        return self._config



    def build_request(
        self,
        context: RequestContext,
    ) -> DownloadRequest:

        return DownloadRequest.from_context(
            context,
        )