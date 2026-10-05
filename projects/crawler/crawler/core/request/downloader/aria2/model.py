from dataclasses import dataclass
from enum import Enum
from typing import Any, TypeGuard


@dataclass(frozen=True, slots=True)
class Aria2DownloadHandle:
    gid: str



class Aria2Status(str,Enum):
    ACTIVE = "active"
    WAITING = "waiting"
    PAUSED = "paused"
    COMPLETE = "complete"
    ERROR = "error"
    REMOVED = "removed"

@dataclass(frozen=True, slots=True)
class Aria2File:
    path: str
    length: int
    completed_length: int
    selected: bool
    # uris: str
    # index: int


    @property
    def is_complete(self) -> bool:
        return (
            self.length == self.completed_length
        )

@dataclass(frozen=True, slots=True)
class Aria2DownloadStatus:
    gid: str
    status: Aria2Status

    total_length: int
    completed_length: int

    download_speed: int
    upload_speed: int

    connections: int

    error_code: str | None = None
    error_message: str | None = None

    dir: str | None = None
    files: tuple[Aria2File, ...] = ()

    @property
    def is_finished(self) -> bool:
        return self.status in {
            Aria2Status.COMPLETE,
            Aria2Status.ERROR,
            Aria2Status.REMOVED,
        }

    @property
    def is_success(self) -> bool:
        return self.status is Aria2Status.COMPLETE

    @property
    def progress(self) -> float | None:
        if self.total_length <= 0:
            return None

        return (
            self.completed_length
            / self.total_length
        )

@dataclass(frozen=True, slots=True)
class Aria2DownloadResult:
    gid: str
    status: Aria2DownloadStatus
    files: tuple[Aria2File, ...]
    error_code: str | None = None
    error_message: str | None = None

JsonObject = dict[str, Any]


def is_json_object(
    value: Any,
) -> TypeGuard[JsonObject]:
    return isinstance(value, dict)