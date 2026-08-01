from dataclasses import dataclass

from models.enums.downloader_type import DownloaderType
from models.enums.response_format import ResponseFormat


@dataclass(slots=True, frozen=True)
class RequestProfile:

    downloader: DownloaderType

    response_format: ResponseFormat