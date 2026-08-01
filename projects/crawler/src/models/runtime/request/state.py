from dataclasses import dataclass


@dataclass(slots=True)
class RequestState:

    retries: int = 0

    downloaded: bool = False

    started_at: float | None = None

    finished_at: float | None = None