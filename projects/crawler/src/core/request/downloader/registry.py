from __future__ import annotations

from core.registry import Registry
from core.request.typing import DownloaderType

from .plugin import DownloaderPlugin


class DownloaderRegistry(
    Registry[
        DownloaderType,
        DownloaderPlugin,
    ],
):
    """
    Registry of downloader implementations.
    """

    pass