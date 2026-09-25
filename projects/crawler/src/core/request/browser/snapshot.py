from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BrowserPageSnapshot:

    url: str
    title: str
    content: str
    status_code: int | None