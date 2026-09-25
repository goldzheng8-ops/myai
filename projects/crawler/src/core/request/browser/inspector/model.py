from dataclasses import dataclass

from core.request.browser.typing import BrowserPageState

@dataclass(frozen=True, slots=True)
class BrowserPageInspection:

    state: BrowserPageState

    url: str

    title: str

    reason: str | None = None