from abc import ABC, abstractmethod
from dataclasses import dataclass
from core.request.browser.snapshot import BrowserPageSnapshot


@dataclass(frozen=True, slots=True)
class BrowserPageStabilityPolicy(
    ABC,
):

    interval: float

    max_attempts: int

    @abstractmethod
    def is_stable(
        self,
        previous: BrowserPageSnapshot,
        current: BrowserPageSnapshot,
    ) -> bool:
        raise NotImplementedError