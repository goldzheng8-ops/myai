from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DownloaderCapabilities:

    supports_resumable: bool = False
    supports_streaming: bool = False